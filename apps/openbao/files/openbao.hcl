# Rendered by NepFleet. No secret is in here: OpenBao's own keys come from
# `bao operator init`, which you run yourself (see the template's notes).
storage "raft" {
  path    = "/openbao/file"
  node_id = "openbao"
}

# Plain HTTP on the ingress network: Caddy terminates TLS for the domain.
listener "tcp" {
  address     = "0.0.0.0:8200"
  tls_disable = true
}

api_addr      = "${NEPFLEET_URL}"
cluster_addr  = "http://127.0.0.1:8201"
ui            = true
disable_mlock = true
