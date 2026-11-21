# Rendered by NepFleet. No secret is in here: the unseal key and the admin's
# password reach OpenBao as environment variables (see compose.yaml).
storage "raft" {
  path    = "/openbao/file"
  node_id = "openbao"
}

# Plain HTTP on the ingress network: Caddy terminates TLS for the domain.
listener "tcp" {
  address     = "0.0.0.0:8200"
  tls_disable = true
}

# Auto-unseal with a key NepFleet generated (hex, 32 bytes): OpenBao unseals
# itself on every start, so a restart or an image update needs nobody.
seal "static" {
  current_key_id = "nepfleet-1"
  current_key    = "env://BAO_UNSEAL_KEY"
}

# Runs once, on the very first start (empty storage): initialises OpenBao,
# creates the admin from the stack's inputs, and revokes the root token it
# used. Changing it later has no effect.
initialize "admin" {
  request "admin-policy" {
    operation = "update"
    path      = "sys/policies/acl/admin"
    data = {
      policy = <<EOP
path "*" {
  capabilities = ["create", "read", "update", "patch", "delete", "list", "scan", "sudo"]
}
EOP
    }
  }

  request "mount-userpass" {
    operation = "update"
    path      = "sys/auth/userpass"
    data = {
      type        = "userpass"
      description = "The admin from the stack's inputs."
    }
  }

  request "admin-user" {
    operation = "update"
    path      = "auth/userpass/users/${ADMIN_USER}"
    data = {
      password = {
        eval_source     = "env"
        eval_type       = "string"
        env_var         = "BAO_ADMIN_PASSWORD"
        require_present = true
      }
      token_policies = ["admin"]
    }
  }
}

api_addr      = "${NEPFLEET_URL}"
cluster_addr  = "http://127.0.0.1:8201"
ui            = true
disable_mlock = true
