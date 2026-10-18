import threading
import time
import pytest

from idl_backend.contracts.client import request_json, ServiceError
from idl_backend.contracts.courses import Course
from idl_backend.local.http import create_server

UUID = "80396753-7fc8-4f55-9188-bddbdb828169"


@pytest.fixture
def server():
    courses = {UUID: Course(UUID, "test-course", "/modules/test-course")}
    http = create_server(port=0, courses=courses, token="test-token")
    thread = threading.Thread(target=http.serve_forever, daemon=True)
    thread.start()
    yield "http://127.0.0.1:" + str(http.server_port)
    http.shutdown()
    http.server_close()
    http.jobs.close()
    thread.join()


def test_manual_native_service_implements_cloud_job_protocol(server):
    payload = {"course_uuid": UUID, "endpoint": "/lenet5/fixed-kernel-preview", "payload": {"image": [[0] * 28 for _ in range(28)]}}
    payload["cache_context"] = {"course_scope": "official/visual-feature-learning", "endpoint": payload["endpoint"], "request_data": payload["payload"]}
    created = request_json(server, "test-token", "POST", "/v1/jobs", payload)
    record = request_json(server, "test-token", "GET", "/v1/jobs/" + created["id"] + "/wait?timeout=25", timeout=30)
    assert record["status"] == "complete", record
    assert record["result"]["result"]["dataset"]["images"] == "custom-canvas"
    outbox = request_json(server, "test-token", "GET", "/v1/completions")
    assert outbox["records"][0]["cache_context"] == payload["cache_context"]
    request_json(server, "test-token", "POST", "/v1/completions/" + created["id"] + "/ack", {})
    assert request_json(server, "test-token", "GET", "/v1/completions") == {"records": []}


def test_auth_and_unknown_course_rejected(server):
    with pytest.raises(ServiceError) as error:
        request_json(server, "wrong", "GET", "/v1/endpoints")
    assert error.value.status == 401
    with pytest.raises(ServiceError) as error:
        request_json(server, "test-token", "POST", "/v1/jobs", {"course_uuid": "not-registered", "endpoint": "/lenet5/fixed-kernel-preview"})
    assert error.value.status == 422


def test_wait_rejects_unknown_jobs_and_invalid_timeout(server):
    for suffix, status in [("/wait", 404), ("/wait?timeout=nan", 422), ("/wait?timeout=0", 422)]:
        with pytest.raises(ServiceError) as error:
            request_json(server, "test-token", "GET", "/v1/jobs/unknown" + suffix)
        assert error.value.status == status


def test_dev_mode_is_explicit_and_loopback_only():
    with pytest.raises(ValueError):
        create_server("0.0.0.0", 0, token="", dev=True)
    with pytest.raises(ValueError):
        create_server(port=0, token="")

