# Design

One shared feature policy runs against a camera capability port. Both model
compositions must preserve existing behavior. Unsupported hardware returns a
typed capability result rather than silently no-oping or simulating the
feature.
