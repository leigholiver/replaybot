resource "cloudflare_worker_route" "cf_route_www_redirects" {
  count       = length(var.www_redirects)
  zone_id     = var.cloudflare_zone
  pattern     = "${var.www_redirects[count.index].from}/*"
  script_name = cloudflare_worker_script.cf_script_www_redirects[count.index].name
}

resource "cloudflare_worker_script" "cf_script_www_redirects" {
  count   = length(var.www_redirects)
  name    = "${var.project_name}_${var.name}_${count.index}_www_redirects"
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

    // redirect www to non www based on domain name
    if(request.url.startsWith("https://${var.www_redirects[count.index].from}")) {
      loc = request.url.replace("https://${var.www_redirects[count.index].from}", "https://${var.www_redirects[count.index].to}")
      return Response.redirect(loc, 307) 
    }
  return fetch(request)
}
EOF
}