# Dashboard composition contract

`app.py` owns dashboard composition. Beta and main use their checked-in
environment configuration. Staff-created preview users may sign in on beta;
preview login remains disabled on main.

The user-visible promise is that an eligible preview user can reach the summary
in beta, while main continues to show sign-in. The focused seam spans
environment configuration, `compose()`, and `Dashboard.summary()`.

`test_dashboard.py` is the existing component check. Final matrix execution is
separate from routine focused verification.
