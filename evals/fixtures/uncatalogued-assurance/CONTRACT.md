# Document download contract
Authenticated members may download only files beneath their own workspace root.
The storage root is per member. The query string is attacker controlled and may
contain absolute paths, dot segments, or symlink names. Neighboring files can
contain another member's private material. The existing storage.resolve_member_file
validates containment after resolution and returns an opened authorized handle.
