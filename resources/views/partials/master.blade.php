<!DOCTYPE html>
<html lang="en">

<head>
    <title>Tosca</title>
    <meta charset="utf-8">
    <meta content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0" name="viewport" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />
    <!-- Favicons -->
    <link rel="apple-touch-icon" href="{{ asset("/assets/img/kit/free/apple-icon.png") }}">
    <link rel="icon" href="{{ asset("/assets/img/kit/free/favicon.png") }}">
    <title>
        Landing &#45; Material Kit by Creative Tim
    </title>
    <!--     Fonts and icons     -->
    <link rel="stylesheet" type="text/css" href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700|Roboto+Slab:400,700|Material+Icons" />
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/latest/css/font-awesome.min.css" />
    <link rel="stylesheet" href="{{ asset("/assets/css/material-kit.css?v=2.0.2") }}">
    <!-- Documentation extras -->
    <!-- CSS Just for demo purpose, don't include it in your project -->
    <link href="{{ asset("/assets/assets-for-demo/demo.css") }}" rel="stylesheet" />
    <!-- iframe removal -->
</head>


<body class="landing-page ">
    @yield('content')

    <!--   Core JS Files   -->
    <script src="{{ asset("/assets/js/core/jquery.min.js") }}"></script>
    <script src="{{ asset("/assets/js/core/popper.min.js") }}"></script>
    <script src="{{ asset("/assets/js/bootstrap-material-design.js") }}"></script>
    <!--  Plugin for Date Time Picker and Full Calendar Plugin  -->
    <script src="{{ asset("/assets/js/plugins/moment.min.js") }}"></script>
    <!--    Plugin for the Datepicker, full documentation here: https://github.com/Eonasdan/bootstrap-datetimepicker -->
    <script src="{{ asset("/assets/js/plugins/bootstrap-datetimepicker.min.jssss") }}"></script>
    <!--    Plugin for the Sliders, full documentation here: http://refreshless.com/nouislider/ -->
    <script src="{{ asset("/assets/js/plugins/nouislider.min.js") }}"></script>
    <!-- Material Kit Core initialisations of plugins and Bootstrap Material Design Library -->
    <script src="{{ asset("/assets/js/material-kit.js?v=2.0.2") }}"></script>
    <!-- Fixed Sidebar Nav - js With initialisations For Demo Purpose, Don't Include it in your project -->
    <script src="{{ asset("/assets/assets-for-demo/js/material-kit-demo.js") }}"></script>
</body>

