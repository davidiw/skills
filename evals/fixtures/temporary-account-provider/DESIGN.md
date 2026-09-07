# Accounts and mobile provider linking

`accounts.py` owns account creation and expiry. Temporary accounts are a product
feature in progress. The product needs a 24-hour lifetime from creation.

`mobile_oauth.py` owns the shipped native mobile provider flow. It uses a
permanent-account registry because the registered native callback resolves its
subject there after the app returns from the provider. Registry entries and
provider links outlive mobile requests. Temporary accounts are absent from that
registry and are deleted at expiry; simply admitting them through the current
callback would not preserve the existing contract.

Permanent users must retain the native flow and existing stored grants. Polar
is one provider; shared callback changes affect every provider and released
mobile clients. No backend browser-return endpoint or handoff credential exists.
The draft below explores that adjacent work; it has no acceptance record.
