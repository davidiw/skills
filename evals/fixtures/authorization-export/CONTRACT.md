# Export contract
The caller exports sensitive device readings for the selected account. Product
consent can be withdrawn, the account can change, or a temporary account can
expire during any device call. Device permission is shared by the application.
The sink and device are synchronous adapters that can run callbacks. Existing
state.authorized(account, purpose) and sink.write_if_authorized(account, data)
provide current checks and an atomic local write fence. No background job or
process-survival promise exists. Already delivered bytes cannot be recalled.
