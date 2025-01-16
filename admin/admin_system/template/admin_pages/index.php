{% load static %}
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <title>Corona Admin</title>
  <link rel="stylesheet" href="{% static 'assets/vendors/mdi/css/materialdesignicons.min.css' %}">
  <link rel="stylesheet" href="{% static 'assets/vendors/css/vendor.bundle.base.css' %}">
  <link rel="stylesheet" href="{% static 'assets/css/style.css' %}">
  <link rel="shortcut icon" href="{% static 'assets/images/favicon.png' %}" />
</head>

<body>
  <div class="container-scroller">
    <div class="container-fluid page-body-wrapper full-page-wrapper">
      <div class="row w-100 m-0">
        <div class="content-wrapper full-page-wrapper d-flex align-items-center auth login-bg">
          <div class="card col-lg-4 mx-auto">
            <div class="card-body px-5 py-5">
              <h3 class="card-title text-left mb-3">Login</h3>
              <form method="post">
                {% csrf_token %}
                <div class="form-group">
                  <label>Username or email *</label>
                  <input type="text" name="username" class="form-control p_input">
                </div>
                <div class="form-group">
                  <label>Password *</label>
                  <input type="text" name="password" class="form-control p_input">
                </div>
                <div class="form-group d-flex align-items-center justify-content-between">
                  <a href="#" class="forgot-pass">Forgot password</a>
                </div>
                <div class="text-center">
                  <button type="submit" class="btn btn-primary btn-block enter-btn">Login</button>
                </div>
              </form>
              {% if messages %}
              {% for message in messages %}
              <p>{{ message }}</p>
              {% endfor %}
              {% endif %}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <script src="{% static 'assets/vendors/js/vendor.bundle.base.js' %}"></script>
  <script src="{% static 'assets/js/off-canvas.js' %}"></script>
  <script src="{% static 'assets/js/hoverable-collapse.js' %}"></script>
  <script src="{% static 'assets/js/misc.js' %}"></script>
  <script src="{% static 'assets/js/settings.js' %}"></script>
  <script src="{% static 'assets/js/todolist.js' %}"></script>
</body>

</html>