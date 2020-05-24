resource "cloudflare_worker_route" "cf_route_api_redirects" {
  count       = length(var.api_redirects)
  zone_id     = var.cloudflare_zone
  pattern     = "${var.api_redirects[count.index].from}/*"
  script_name = cloudflare_worker_script.cf_script_api_redirects[count.index].name
}

resource "cloudflare_worker_script" "cf_script_api_redirects" {
  count   = length(var.api_redirects)
  name    = "${var.project_name}_${var.name}_${count.index}_api_redirects"
  content = <<EOF
addEventListener('fetch', event => {
  event.respondWith(bulkRedirects(event.request))
})

async function bulkRedirects(request) {
    // force https
    if(request.url.startsWith("http://")) {
        return getResponse(request.url.replace("http://", "https://"));
    }

    // redirect www to non www based on domain name
    if(request.url.startsWith("https://${var.api_redirects[count.index].from}")) {
        return getResponse(request.url.replace("https://${var.api_redirects[count.index].from}", "${var.api_redirects[count.index].to}"))
    }
  return fetch(request)
}

// Add an access-control-allow-origin header so that the s3 bucket website api requests work with cors
function getResponse(location) {
    response = new Response("", { 'status': 307 });
    response.headers.set('Location', location);
    response.headers.set('Access-Control-Allow-Origin', '*');
    return response;
}
EOF
}