{% load static %}

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Admin</title>
    <link rel="stylesheet" href="{% static 'assets/vendors/mdi/css/materialdesignicons.min.css' %}">
    <link rel="stylesheet" href="{% static 'assets/vendors/css/vendor.bundle.base.css' %}">
    <link rel="stylesheet" href="{% static 'assets/vendors/jvectormap/jquery-jvectormap.css' %}">
    <link rel="stylesheet" href="{% static 'assets/vendors/flag-icon-css/css/flag-icon.min.css' %}">
    <link rel="stylesheet" href="{% static 'assets/vendors/owl-carousel-2/owl.carousel.min.css' %}">
    <link rel="stylesheet" href="{% static 'assets/vendors/owl-carousel-2/owl.theme.default.min.css' %}">
    <link rel="stylesheet" href="{% static 'assets/css/style.css' %}">
    <link rel="shortcut icon" href="{% static 'assets/images/favicon.png' %}" />
</head>

<body>
    <div class="container-scroller">
        <nav class="sidebar sidebar-offcanvas" id="sidebar">
            <div class="sidebar-brand-wrapper d-none d-lg-flex align-items-center justify-content-center fixed-top">
                <a class="sidebar-brand brand-logo" href="{% url 'dashboard' %}"><img src="{% static 'assets/images/logo.svg' %}" alt="logo" /></a>
                <a class="sidebar-brand brand-logo-mini" href="{% url 'dashboard' %}"><img src="{% static 'assets/images/logo-mini.svg' %}" alt="logo" /></a>
            </div>
            <ul class="nav">
                <li class="nav-item profile">
                    <div class="profile-desc">
                        <div class="profile-pic">
                            <div class="count-indicator">
                                <img class="img-xs rounded-circle " src="{% static 'assets/images/faces/face15.jpg' %}" alt="">
                                <span class="count bg-success"></span>
                            </div>
                            <div class="profile-name">
                                <h5 class="mb-0 font-weight-normal">{{ user.username }}</h5>
                                <span>{{ role }}</span>
                            </div>
                        </div>
                    </div>
                </li>
                <li class="nav-item nav-category">
                    <span class="nav-link">Navigation</span>
                </li>
                <li class="nav-item menu-items">
                    <a class="nav-link" href="{% url 'dashboard' %}">
                        <span class="menu-icon">
                            <i class="mdi mdi-speedometer"></i>
                        </span>
                        <span class="menu-title">Dashboard</span>
                    </a>
                </li>
                <li class="nav-item menu-items">
                    <a class="nav-link" href="{% url 'attendance' %}">
                        <span class="menu-icon">
                            <i class="mdi mdi-laptop"></i>
                        </span>
                        <span class="menu-title">Attendance</span>
                    </a>
                </li>
                {% if user.role == 'Super Admin' %}
                <li class="nav-item menu-items">
                    <a class="nav-link" href="{% url 'management' %}">
                        <span class="menu-icon">
                            <i class="mdi mdi-playlist-play"></i>
                        </span>
                        <span class="menu-title">User Management</span>
                    </a>
                </li>
                <li class="nav-item menu-items">
                    <a class="nav-link" href="{% url 'student' %}">
                        <span class="menu-icon">
                            <i class="mdi mdi-contacts"></i>
                        </span>
                        <span class="menu-title">Student Management</span>
                    </a>
                </li>
                {% endif %}
                <li class="nav-item menu-items">
                    <a class="nav-link" data-toggle="collapse" href="#subjects" aria-expanded="false" aria-controls="subjects">
                        <span class="menu-icon">
                            <i class="mdi mdi-table-large"></i>
                        </span>
                        <span class="menu-title">Subjects / Enroll</span>
                        <i class="menu-arrow"></i>
                    </a>
                    <div class="collapse" id="subjects">
                        <ul class="nav flex-column sub-menu">
                            <li class="nav-item"> <a class="nav-link" href="{% url 'subject' %}"> Subjects </a></li>
                            <li class="nav-item"> <a class="nav-link" href="{% url 'enrollment' %}"> Enrollment </a></li>
                        </ul>
                    </div>
                </li>
            </ul>
        </nav>
        <div class="container-fluid page-body-wrapper">
            <nav class="navbar p-0 fixed-top d-flex flex-row">
                <div class="navbar-brand-wrapper d-flex d-lg-none align-items-center justify-content-center">
                    <a class="navbar-brand brand-logo-mini" href="{% url 'dashboard' %}"><img src="{% static 'assets/images/logo-mini.svg' %}" alt="logo" /></a>
                </div>
                <div class="navbar-menu-wrapper flex-grow d-flex align-items-stretch">
                    <button class="navbar-toggler navbar-toggler align-self-center" type="button" data-toggle="minimize">
                        <span class="mdi mdi-menu"></span>
                    </button>
                    <ul class="navbar-nav navbar-nav-right">
                        <li class="nav-item dropdown">
                            <a class="nav-link" id="profileDropdown" href="#" data-toggle="dropdown">
                                <div class="navbar-profile">
                                    <img class="img-xs rounded-circle" src="{% static 'assets/images/faces/face15.jpg' %}" alt="">
                                    <p class="mb-0 d-none d-sm-block navbar-profile-name">{{ user.username }}</p>
                                    <i class="mdi mdi-menu-down d-none d-sm-block"></i>
                                </div>
                            </a>
                            <div class="dropdown-menu dropdown-menu-right navbar-dropdown preview-list" aria-labelledby="profileDropdown">
                                <h6 class="p-3 mb-0">Profile</h6>
                                <div class="dropdown-divider"></div>
                                <a class="dropdown-item preview-item" href="{% url 'profile' %}">
                                    <div class="preview-thumbnail">
                                        <div class="preview-icon bg-dark rounded-circle">
                                            <i class="mdi mdi-settings text-success"></i>
                                        </div>
                                    </div>
                                    <div class="preview-item-content">
                                        <p class="preview-subject mb-1">Settings</p>
                                    </div>
                                </a>
                                <div class="dropdown-divider"></div>
                                <a class="dropdown-item preview-item" onclick="logoutUser()" style="cursor: pointer;">
                                    <div class="preview-thumbnail">
                                        <div class="preview-icon bg-dark rounded-circle">
                                            <i class="mdi mdi-logout text-danger"></i>
                                        </div>
                                    </div>
                                    <div class="preview-item-content">
                                        <p class="preview-subject mb-1">Log out</p>
                                    </div>
                                </a>
                            </div>
                        </li>
                    </ul>
                    <button class="navbar-toggler navbar-toggler-right d-lg-none align-self-center" type="button" data-toggle="offcanvas">
                        <span class="mdi mdi-format-line-spacing"></span>
                    </button>
                </div>
            </nav>
            <!-- partial -->
            <div class="main-panel">
                <div class="content-wrapper">
                    <div class="row ">
                        <div class="col-12 grid-margin stretch-card">
                            <div class="card">
                                <div class="card-body">
                                    <h4 class="card-title">Edit Subject</h4>
                                    <p class="card-description"> Edit Course / Subject for Students </p>
                                    <form class="forms-sample" method="POST">
                                        {% csrf_token %}
                                        <div class="form-group">
                                            <label for="courseName">Course Name</label>
                                            <input type="text" class="form-control" id="courseName" name="courseName" placeholder="Course Name" value="{{ subject.name }}" style="color:white;">
                                        </div>
                                        <div class="form-group">
                                            <label for="courseCode">Course Code</label>
                                            <input type="text" class="form-control" id="courseCode" name="courseCode" placeholder="Course Code" value="{{ subject.code }}" style="color:white;">
                                        </div>
                                        <div class="form-group">
                                            <label for="faculty">Faculty</label>
                                            <input type="text" class="form-control" id="faculty" name="faculty" placeholder="Faculty" value="{{ subject.faculty }}" style="color:white;">
                                        </div>
                                        <button type="submit" class="btn btn-primary mr-2">Submit</button>
                                        <a class="btn btn-dark" href="{% url 'subject' %}">Cancel</a>
                                    </form>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <footer class="footer">
                    <div class="d-sm-flex justify-content-center justify-content-sm-between">
                    </div>
                </footer>
            </div>
        </div>
    </div>
    <script src="{% static 'assets/vendors/js/vendor.bundle.base.js' %}"></script>
    <script src="{% static 'assets/vendors/chart.js/Chart.min.js' %}"></script>
    <script src="{% static 'assets/vendors/progressbar.js/progressbar.min.js' %}"></script>
    <script src="{% static 'assets/vendors/jvectormap/jquery-jvectormap.min.js' %}"></script>
    <script src="{% static 'assets/vendors/jvectormap/jquery-jvectormap-world-mill-en.js' %}"></script>
    <script src="{% static 'assets/vendors/owl-carousel-2/owl.carousel.min.js' %}"></script>
    <script src="{% static 'assets/js/off-canvas.js' %}"></script>
    <script src="{% static 'assets/js/hoverable-collapse.js' %}"></script>
    <script src="{% static 'assets/js/misc.js' %}"></script>
    <script src="{% static 'assets/js/settings.js' %}"></script>
    <script src="{% static 'assets/js/todolist.js' %}"></script>
    <script src="{% static 'assets/js/dashboard.js' %}"></script>
</body>

</html>

<script>
    function logoutUser() {
        if (confirm("Are you sure you want to log out?")) {
            fetch("{% url 'logout' %}", {
                method: "POST",
                headers: {
                    "X-CSRFToken": "{{ csrf_token }}"
                }
            }).then(response => {
                if (response.ok) {
                    window.location.href = "{% url 'login' %}";
                } else {
                    alert("Logout failed. Please try again.");
                }
            }).catch(error => {
                console.error("Error during logout:", error);
            });
        }
    }

    document.querySelectorAll('.dropdown-item').forEach(item => {
        item.addEventListener('click', event => {
            const value = event.target.getAttribute('data-value');
            document.getElementById('roleInput').value = value;
            document.getElementById('role').innerText = value;
        });
    });

    document.getElementById('role').innerText = document.getElementById('roleInput').value;
</script>