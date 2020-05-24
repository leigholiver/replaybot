resource "cloudflare_worker_route" "cf_route_domain" {
  zone_id     = var.cloudflare_zone
  pattern     = "${var.domain_name}/*"
  script_name = cloudflare_worker_script.cf_script_domain.name
}

resource "cloudflare_worker_script" "cf_script_domain" {
  name    = "${var.project_name}_${var.name}_domain"
  content = <<EOF
addEventListener('fetch', event => {
  event.respondWith(bulkRedirects(event.request))
})

async function bulkRedirects(request) {
    // force https
    if(request.url.startsWith("http://")) {
      loc = request.url.replace("http://", "https://")
      return Response.redirect(loc, 307) 
    }

    %{if length(var.allowed_ips) > 0}
      // make sure we're allowed access
      const client_ip = request.headers.get('CF-Connecting-IP');
      const allowed_ips = [%{for index, ip in var.allowed_ips}
          "${ip}"%{if index < length(var.allowed_ips) - 1},%{endif}%{endfor}
      ];

      if(!isIp4InCidrs(client_ip, allowed_ips) && !allowed_ips.includes(client_ip)) {
        return new Response("Forbidden", {status: 403});
      }
    %{endif}

  return fetch(request)
}


// cidr checking functions from https://tech.mybuilder.com/determining-if-an-ipv4-address-is-within-a-cidr-range-in-javascript/
const ip4ToInt = ip => ip.split('.').reduce((int, oct) => (int << 8) + parseInt(oct, 10), 0) >>> 0;

const isIp4InCidr = ip => cidr => {
  const [range, bits = 32] = cidr.split('/');
  const mask = ~(2 ** (32 - bits) - 1);
  return (ip4ToInt(ip) & mask) === (ip4ToInt(range) & mask);
};

const isIp4InCidrs = (ip, cidrs) => cidrs.some(isIp4InCidr(ip));
EOF
}