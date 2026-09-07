# Screen contract
Only current-account results may be painted. AccountFence.publish_if_current is
the established atomic guard; caller code must use it after an asynchronous read.
The data service already checks read authorization. The bug is a screen bypass
of the unchanged guard, not a request to redesign credentials or access policy.
