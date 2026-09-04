# Runtime Ownership

Wake recognition owns its live audio buffers. Google authorization owns its
transient authorization buffers. Preview is optional and reclaimable. The
composition root starts each activity, but there is no shared admission policy.
