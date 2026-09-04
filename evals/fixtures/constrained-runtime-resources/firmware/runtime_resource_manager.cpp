bool start_wake_recognition();
bool start_google_authorization();
bool start_preview();

void on_allocation_failed() {
  restart_device();
}
