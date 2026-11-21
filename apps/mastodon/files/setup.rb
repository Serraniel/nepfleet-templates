# frozen_string_literal: true

# Run once per start by the setup service (`rails runner`), after the database
# migrations and before web and sidekiq start.
#
# 1. Push notification (VAPID) keys: made once and kept in the vapid volume,
#    which web and sidekiq read on start. A key pair given in the stack's
#    inputs wins. The keys must never change later: browsers subscribed to
#    the old ones would stop getting notifications.
# 2. The owner account from the stack's inputs, the way `tootctl accounts
#    create USER --email … --confirmed --approve --role Owner` makes it, but
#    with the password the user typed instead of a random one nobody can read.
#    When the username already has an account nothing is changed, so a
#    password changed in Mastodon later stays as it is.

vapid = '/vapid/vapid.env'
unless File.size?(vapid)
  key = Webpush.generate_key
  File.write("#{vapid}.tmp", "VAPID_PRIVATE_KEY=#{key.private_key}\nVAPID_PUBLIC_KEY=#{key.public_key}\n")
  File.chmod(0o440, "#{vapid}.tmp")
  File.chown(991, 991, "#{vapid}.tmp") # the mastodon user of web and sidekiq
  File.rename("#{vapid}.tmp", vapid)
  puts 'setup: made the push notification keys'
end

username = ENV.fetch('ADMIN_USER')
email = ENV.fetch('ADMIN_EMAIL')
password = ENV.fetch('ADMIN_PASSWORD')

if Account.find_local(username)&.user.present?
  puts "setup: the account #{username} exists, leaving it as it is"
  exit 0
end

role = UserRole.find_by!(name: 'Owner')
user = User.new(
  email: email,
  password: password,
  password_confirmation: password,
  agreement: true,
  role_id: role.id,
  confirmed_at: Time.now.utc,
  bypass_registration_checks: true
)
user.account = Account.new(username: username)
# Sign-ups must show their mail domain has a mail server (an MX lookup); the
# owner, set by whoever runs the server, need not: a home lab's domain often
# has none, and the lookup fails where the host has no outside DNS.
user.define_singleton_method(:validate_email_dns?) { false }

unless user.save
  warn "setup: cannot create the account #{username}: #{user.errors.full_messages.join('; ')}"
  exit 1
end

user.confirmed_at = nil
user.mark_email_as_confirmed!
user.approve!
puts "setup: created the owner account #{username}"
