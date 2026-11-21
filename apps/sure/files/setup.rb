# Creates the stack's first account, a super admin in a new family, from
# ADMIN_EMAIL and ADMIN_PASSWORD, so sign-up never has to be open for it.
# Runs after every start of the stack and does nothing once any account
# exists: it neither changes that account nor adds a second one.
email = ENV.fetch("ADMIN_EMAIL").strip.downcase
password = ENV.fetch("ADMIN_PASSWORD")

User.transaction do
  # Sure's own lock for picking the first user's role, so a sign-up at the
  # same moment cannot also become the first account.
  User.lock_first_user_role!

  if User.exists?
    puts "Sure already has an account; no admin created."
  else
    User.create!(
      family: Family.new,
      email: email,
      password: password,
      role: :super_admin
    )
    puts "Created the admin #{email}."
  end
end
