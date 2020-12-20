addEventListener('fetch', event => {
    event.respondWith(checkAllowed(event.request))
})

async function checkAllowed(request) {
    %{if length(allowed_ips) > 0}
    const client_ip = request.headers.get('CF-Connecting-IP');
    const allowed_ips = [%{for index, ip in allowed_ips}
        "${ip}"%{if index < length(allowed_ips) - 1},%{endif}%{endfor}
    ];

    if(!isIp4InCidrs(client_ip, allowed_ips) && !allowed_ips.includes(client_ip)) {
        return new Response("Forbidden", {status: 403});
    }
    %{endif}
    return fetch(request)
}

const ip4ToInt = ip => ip.split('.').reduce((int, oct) => (int << 8) + parseInt(oct, 10), 0) >>> 0;
const isIp4InCidr = ip => cidr => {
    const [range, bits = 32] = cidr.split('/');
    const mask = ~(2 ** (32 - bits) - 1);
    return (ip4ToInt(ip) & mask) === (ip4ToInt(range) & mask);
};
const isIp4InCidrs = (ip, cidrs) => cidrs.some(isIp4InCidr(ip));
