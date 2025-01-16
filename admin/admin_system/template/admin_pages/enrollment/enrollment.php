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
                                <h5 class="mb-0 font-weight-normal">Henry Klein</h5>
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
                    <a class="nav-link" href="#ui-basic">
                        <span class="menu-icon">
                            <i class="mdi mdi-laptop"></i>
                        </span>
                        <span class="menu-title">Basic UI Elements</span>
                    </a>
                </li>
                <li class="nav-item menu-items">
                    <a class="nav-link" href="pages/forms/basic_elements.html">
                        <span class="menu-icon">
                            <i class="mdi mdi-playlist-play"></i>
                        </span>
                        <span class="menu-title">Form Elements</span>
                    </a>
                </li>
                <li class="nav-item menu-items">
                    <a class="nav-link" href="pages/tables/basic-table.html">
                        <span class="menu-icon">
                            <i class="mdi mdi-table-large"></i>
                        </span>
                        <span class="menu-title">Tables</span>
                    </a>
                </li>
                <li class="nav-item menu-items">
                    <a class="nav-link" href="pages/charts/chartjs.html">
                        <span class="menu-icon">
                            <i class="mdi mdi-chart-bar"></i>
                        </span>
                        <span class="menu-title">Charts</span>
                    </a>
                </li>
                <li class="nav-item menu-items">
                    <a class="nav-link" href="pages/icons/mdi.html">
                        <span class="menu-icon">
                            <i class="mdi mdi-contacts"></i>
                        </span>
                        <span class="menu-title">Icons</span>
                    </a>
                </li>
                <li class="nav-item menu-items">
                    <a class="nav-link" data-toggle="collapse" href="#auth" aria-expanded="false" aria-controls="auth">
                        <span class="menu-icon">
                            <i class="mdi mdi-security"></i>
                        </span>
                        <span class="menu-title">User Pages</span>
                        <i class="menu-arrow"></i>
                    </a>
                    <div class="collapse" id="auth">
                        <ul class="nav flex-column sub-menu">
                            <li class="nav-item"> <a class="nav-link" href="pages/samples/blank-page.html"> Blank Page </a></li>
                            <li class="nav-item"> <a class="nav-link" href="pages/samples/error-404.html"> 404 </a></li>
                            <li class="nav-item"> <a class="nav-link" href="pages/samples/error-500.html"> 500 </a></li>
                            <li class="nav-item"> <a class="nav-link" href="pages/samples/login.html"> Login </a></li>
                            <li class="nav-item"> <a class="nav-link" href="pages/samples/register.html"> Register </a></li>
                        </ul>
                    </div>
                </li>
                <li class="nav-item menu-items">
                    <a class="nav-link" href="{% url 'documentation' %}">
                        <span class="menu-icon">
                            <i class="mdi mdi-file-document-box"></i>
                        </span>
                        <span class="menu-title">Documentation</span>
                    </a>
                </li>
            </ul>
        </nav>
        <!-- partial -->
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
                        <li class="nav-item dropdown d-none d-lg-block">
                            <a class="nav-link btn btn-success create-new-button" id="createbuttonDropdown" data-toggle="dropdown" aria-expanded="false" href="#">+ Create New Project</a>
                            <div class="dropdown-menu dropdown-menu-right navbar-dropdown preview-list" aria-labelledby="createbuttonDropdown">
                                <h6 class="p-3 mb-0">Projects</h6>
                                <div class="dropdown-divider"></div>
                                <a class="dropdown-item preview-item">
                                    <div class="preview-thumbnail">
                                        <div class="preview-icon bg-dark rounded-circle">
                                            <i class="mdi mdi-file-outline text-primary"></i>
                                        </div>
                                    </div>
                                    <div class="preview-item-content">
                                        <p class="preview-subject ellipsis mb-1">Software Development</p>
                                    </div>
                                </a>
                                <div class="dropdown-divider"></div>
                                <a class="dropdown-item preview-item">
                                    <div class="preview-thumbnail">
                                        <div class="preview-icon bg-dark rounded-circle">
                                            <i class="mdi mdi-web text-info"></i>
                                        </div>
                                    </div>
                                    <div class="preview-item-content">
                                        <p class="preview-subject ellipsis mb-1">UI Development</p>
                                    </div>
                                </a>
                                <div class="dropdown-divider"></div>
                                <a class="dropdown-item preview-item">
                                    <div class="preview-thumbnail">
                                        <div class="preview-icon bg-dark rounded-circle">
                                            <i class="mdi mdi-layers text-danger"></i>
                                        </div>
                                    </div>
                                    <div class="preview-item-content">
                                        <p class="preview-subject ellipsis mb-1">Software Testing</p>
                                    </div>
                                </a>
                                <div class="dropdown-divider"></div>
                                <p class="p-3 mb-0 text-center">See all projects</p>
                            </div>
                        </li>
                        <li class="nav-item nav-settings d-none d-lg-block">
                            <a class="nav-link" href="#">
                                <i class="mdi mdi-view-grid"></i>
                            </a>
                        </li>
                        <li class="nav-item dropdown border-left">
                            <a class="nav-link count-indicator dropdown-toggle" id="messageDropdown" href="#" data-toggle="dropdown" aria-expanded="false">
                                <i class="mdi mdi-email"></i>
                                <span class="count bg-success"></span>
                            </a>
                            <div class="dropdown-menu dropdown-menu-right navbar-dropdown preview-list" aria-labelledby="messageDropdown">
                                <h6 class="p-3 mb-0">Messages</h6>
                                <div class="dropdown-divider"></div>
                                <a class="dropdown-item preview-item">
                                    <div class="preview-thumbnail">
                                        <img src="{% static 'assets/images/faces/face4.jpg' %}" alt="image" class="rounded-circle profile-pic">
                                    </div>
                                    <div class="preview-item-content">
                                        <p class="preview-subject ellipsis mb-1">Mark send you a message</p>
                                        <p class="text-muted mb-0"> 1 Minutes ago </p>
                                    </div>
                                </a>
                                <div class="dropdown-divider"></div>
                                <a class="dropdown-item preview-item">
                                    <div class="preview-thumbnail">
                                        <img src="{% static 'assets/images/faces/face2.jpg' %}" alt="image" class="rounded-circle profile-pic">
                                    </div>
                                    <div class="preview-item-content">
                                        <p class="preview-subject ellipsis mb-1">Cregh send you a message</p>
                                        <p class="text-muted mb-0"> 15 Minutes ago </p>
                                    </div>
                                </a>
                                <div class="dropdown-divider"></div>
                                <a class="dropdown-item preview-item">
                                    <div class="preview-thumbnail">
                                        <img src="{% static 'assets/images/faces/face3.jpg' %}" alt="image" class="rounded-circle profile-pic">
                                    </div>
                                    <div class="preview-item-content">
                                        <p class="preview-subject ellipsis mb-1">Profile picture updated</p>
                                        <p class="text-muted mb-0"> 18 Minutes ago </p>
                                    </div>
                                </a>
                                <div class="dropdown-divider"></div>
                                <p class="p-3 mb-0 text-center">4 new messages</p>
                            </div>
                        </li>
                        <li class="nav-item dropdown border-left">
                            <a class="nav-link count-indicator dropdown-toggle" id="notificationDropdown" href="#" data-toggle="dropdown">
                                <i class="mdi mdi-bell"></i>
                                <span class="count bg-danger"></span>
                            </a>
                            <div class="dropdown-menu dropdown-menu-right navbar-dropdown preview-list" aria-labelledby="notificationDropdown">
                                <h6 class="p-3 mb-0">Notifications</h6>
                                <div class="dropdown-divider"></div>
                                <a class="dropdown-item preview-item">
                                    <div class="preview-thumbnail">
                                        <div class="preview-icon bg-dark rounded-circle">
                                            <i class="mdi mdi-calendar text-success"></i>
                                        </div>
                                    </div>
                                    <div class="preview-item-content">
                                        <p class="preview-subject mb-1">Event today</p>
                                        <p class="text-muted ellipsis mb-0"> Just a reminder that you have an event today </p>
                                    </div>
                                </a>
                                <div class="dropdown-divider"></div>
                                <a class="dropdown-item preview-item">
                                    <div class="preview-thumbnail">
                                        <div class="preview-icon bg-dark rounded-circle">
                                            <i class="mdi mdi-settings text-danger"></i>
                                        </div>
                                    </div>
                                    <div class="preview-item-content">
                                        <p class="preview-subject mb-1">Settings</p>
                                        <p class="text-muted ellipsis mb-0"> Update dashboard </p>
                                    </div>
                                </a>
                                <div class="dropdown-divider"></div>
                                <a class="dropdown-item preview-item">
                                    <div class="preview-thumbnail">
                                        <div class="preview-icon bg-dark rounded-circle">
                                            <i class="mdi mdi-link-variant text-warning"></i>
                                        </div>
                                    </div>
                                    <div class="preview-item-content">
                                        <p class="preview-subject mb-1">Launch Admin</p>
                                        <p class="text-muted ellipsis mb-0"> New admin wow! </p>
                                    </div>
                                </a>
                                <div class="dropdown-divider"></div>
                                <p class="p-3 mb-0 text-center">See all notifications</p>
                            </div>
                        </li>
                        <li class="nav-item dropdown">
                            <a class="nav-link" id="profileDropdown" href="#" data-toggle="dropdown">
                                <div class="navbar-profile">
                                    <img class="img-xs rounded-circle" src="{% static 'assets/images/faces/face15.jpg' %}" alt="">
                                    <p class="mb-0 d-none d-sm-block navbar-profile-name">Henry Klein</p>
                                    <i class="mdi mdi-menu-down d-none d-sm-block"></i>
                                </div>
                            </a>
                            <div class="dropdown-menu dropdown-menu-right navbar-dropdown preview-list" aria-labelledby="profileDropdown">
                                <h6 class="p-3 mb-0">Profile</h6>
                                <div class="dropdown-divider"></div>
                                <a class="dropdown-item preview-item">
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
                                <a class="dropdown-item preview-item">
                                    <div class="preview-thumbnail">
                                        <div class="preview-icon bg-dark rounded-circle">
                                            <i class="mdi mdi-logout text-danger"></i>
                                        </div>
                                    </div>
                                    <div class="preview-item-content" onclick="logoutUser()" style="cursor: pointer;">
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
                    <div class="row">
                        <div class="col-md-12 grid-margin">
                            <div class="card">
                                <div class="card-body">
                                    <h4 class="card-title mb-3">Search Student</h4>
                                    <form method="POST">
                                        {% csrf_token %}
                                        <div class="mb-2">
                                            <input type="text" class="form-control" name="student_id" placeholder="Search Student Id" required style="color: white;">
                                        </div>
                                        <button type="submit" class="btn btn-primary mr-2">Submit</button>
                                    </form>
                                </div>
                            </div>

                            {% if student %}
                            <div class="row mt-3">
                                <div class="col-12 mb-3">
                                    <div class="card">
                                        <div class="card-body">
                                            <h4 class="card-title">Name: {{ student.name }}</h4>
                                            <h4 class="card-title">Student ID: {{ student.enrollment_number }}</h4>
                                            <h4 class="card-title">Faculty: {{ student.faculty }}</h4>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <div>
                                <div class="card">
                                    <div class="card-body">
                                        <div class="d-flex justify-content-between align-items-center">
                                            <h4 class="card-title">Enrollments</h4>
                                            <a class="nav-link btn btn-success create-new-button" id="createEnrollment" href="{% url 'add_enrollment' student.id %}">+ Create Enrollment</a>
                                        </div>
                                        <div class="table-responsive">
                                            <table class="table table-hover">
                                                {% if enrollments %}
                                                <thead>
                                                    <tr>
                                                        <th>Code</th>
                                                        <th>Course Name</th>
                                                        <th>Enrollment Date</th>
                                                        <th>Completed</th>
                                                        <th>Status</th>
                                                    </tr>
                                                </thead>
                                                <tbody>
                                                    {% for enrollment_detail in enrollments %}
                                                    <tr>
                                                        <td>{{ enrollment_detail.subject_code }}</td>
                                                        <td>{{ enrollment_detail.subject_name }}</td>
                                                        <td>{{ enrollment_detail.enrollment.date_enrolled }}</td>
                                                        <td>{{ enrollment_detail.enrollment.date_completed }}</td>
                                                        <td>{% if enrollment_detail.enrollment.status == "Enrolled" %}
                                                            <label class="badge badge-info">{{ enrollment_detail.enrollment.status }}</label>
                                                            {% elif enrollment_detail.enrollment.status == "Completed" %}
                                                            <label class="badge badge-success">{{ enrollment_detail.enrollment.status }}</label>
                                                            {% elif enrollment_detail.enrollment.status == "Canceled" %}
                                                            <label class="badge badge-danger">{{ enrollment_detail.enrollment.status }}</label>
                                                            {% else %}
                                                            <label class="badge badge-warning">{{ enrollment_detail.enrollment.status }}</label>
                                                            {% endif %}
                                                        </td>
                                                        <td class="col-2">
                                                            <a href="{% url 'delete_enrollment' enrollment_detail.enrollment.id %}" type="button" class="btn btn-danger btn-fw">Delete</a>
                                                        </td>
                                                    </tr>
                                                    {% endfor %}
                                                </tbody>
                                                {% else %}
                                                <tr>
                                                    <td colspan="1">No enrollments found.</td>
                                                </tr>
                                                {% endif %}
                                            </table>
                                        </div>
                                    </div>
                                </div>

                            </div>
                            {% endif %}
                            <footer class="footer">

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
</script>