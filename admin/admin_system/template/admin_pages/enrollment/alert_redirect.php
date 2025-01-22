<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Alert</title>
    <script type="text/javascript">
        alert("{{ alert_message }}");
        window.location.href = "{% url redirect_url %}";
    </script>
</head>
<body>
</body>
</html>
