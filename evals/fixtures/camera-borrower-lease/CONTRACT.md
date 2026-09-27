# Camera composition contract

`PreviewSession` acquires and finally closes the camera. Analysis receives an
connected camera for frames and owns its own frame subscription. Pausing either
surface stops its local work. The composition root wires the preview, analysis,
and model port.
