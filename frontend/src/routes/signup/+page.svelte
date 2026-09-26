<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>AeriQ - Sign In / Register</title>

    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: "Inter", "Segoe UI", Arial, sans-serif;
        }

        body {
            min-height: 100vh;
            background: #f5faf7;
            color: #17231d;
        }

        /* ================================
           MAIN PAGE
        ================================= */

        .page {
            min-height: 100vh;
            display: flex;
        }

        /* ================================
           LEFT SECTION
        ================================= */

        .left-section {
            width: 46%;
            min-height: 100vh;

            background:
                radial-gradient(
                    circle at 85% 10%,
                    rgba(20, 180, 120, 0.20),
                    transparent 32%
                ),
                linear-gradient(
                    145deg,
                    #07120f,
                    #0b1d17 55%,
                    #073c2b
                );

            color: white;

            padding: 42px 52px;

            display: flex;
            flex-direction: column;
            justify-content: space-between;

            position: relative;
            overflow: hidden;
        }

        .left-section::before {
            content: "";

            position: absolute;

            width: 420px;
            height: 420px;

            border-radius: 50%;

            background: rgba(17, 163, 110, 0.08);

            top: -180px;
            right: -150px;
        }

        .left-section::after {
            content: "";

            position: absolute;

            width: 350px;
            height: 350px;

            border-radius: 50%;

            background: rgba(17, 163, 110, 0.06);

            bottom: -180px;
            left: -150px;
        }

        /* ================================
           AERIQ LOGO
        ================================= */

        .brand {
            display: flex;
            align-items: center;

            gap: 10px;

            position: relative;
            z-index: 5;
        }

        .brand-icon {
            width: 44px;
            height: 44px;

            border-radius: 12px;

            background: #08a66c;

            display: flex;
            align-items: center;
            justify-content: center;

            box-shadow:
                0 5px 15px rgba(0, 0, 0, 0.25),
                inset 0 0 0 1px rgba(255,255,255,0.08);
        }

        .brand-icon svg {
            width: 29px;
            height: 29px;
        }

        .brand-name {
            color: #ffffff;

            font-size: 24px;

            font-weight: 700;

            letter-spacing: -0.5px;
        }

        /* ================================
           LEFT CONTENT
        ================================= */

        .left-content {
            position: relative;
            z-index: 5;

            max-width: 510px;
        }

        .left-content h1 {
            font-size: 47px;

            line-height: 1.08;

            letter-spacing: -1.8px;

            margin-bottom: 22px;
        }

        .left-content h1 span {
            color: #8eeac4;
        }

        .left-content > p {
            color: #c9e9dc;

            font-size: 16px;

            line-height: 1.7;

            max-width: 470px;

            margin-bottom: 32px;
        }

        /* ================================
           FEATURES
        ================================= */

        .features {
            display: grid;

            grid-template-columns: 1fr 1fr;

            gap: 14px;
        }

        .feature {
            padding: 17px;

            border-radius: 15px;

            background: rgba(255,255,255,0.055);

            border: 1px solid rgba(255,255,255,0.10);

            backdrop-filter: blur(10px);

            transition: 0.25s ease;
        }

        .feature:hover {
            transform: translateY(-3px);

            background: rgba(255,255,255,0.09);
        }

        .feature-icon {
            width: 37px;
            height: 37px;

            border-radius: 10px;

            background: rgba(8,166,108,0.18);

            display: flex;
            align-items: center;
            justify-content: center;

            margin-bottom: 11px;

            font-size: 17px;
        }

        .feature h3 {
            font-size: 14px;

            margin-bottom: 5px;
        }

        .feature p {
            color: #b9d8cc;

            font-size: 11px;

            line-height: 1.5;
        }

        .copyright {
            position: relative;
            z-index: 5;

            color: #8daea1;

            font-size: 11px;
        }

        /* ================================
           RIGHT SECTION
        ================================= */

        .right-section {
            width: 54%;

            min-height: 100vh;

            background: #ffffff;

            padding: 32px 55px;

            display: flex;

            justify-content: center;

            align-items: flex-start;

            overflow-y: auto;
        }

        .auth-wrapper {
            width: 100%;

            max-width: 550px;
        }

        /* ================================
           SECURITY BADGE
        ================================= */

        .top-bar {
            display: flex;

            justify-content: flex-end;

            margin-bottom: 18px;
        }

        .secure-badge {
            display: flex;

            align-items: center;

            gap: 7px;

            padding: 8px 13px;

            background: #effaf5;

            border: 1px solid #d9f1e5;

            color: #087f5b;

            border-radius: 20px;

            font-size: 11px;

            font-weight: 650;
        }

        /* ================================
           AUTH CARD
        ================================= */

        .auth-card {
            border: 1px solid #e3ece7;

            border-radius: 23px;

            padding: 32px;

            box-shadow:
                0 18px 55px rgba(19,67,49,0.08);
        }

        .auth-heading {
            margin-bottom: 23px;
        }

        .auth-heading h2 {
            font-size: 28px;

            color: #15231c;

            margin-bottom: 7px;
        }

        .auth-heading p {
            color: #718078;

            font-size: 13px;
        }

        /* ================================
           TABS
        ================================= */

        .tabs {
            display: grid;

            grid-template-columns: 1fr 1fr;

            background: #f0f6f3;

            padding: 4px;

            border-radius: 11px;

            margin-bottom: 25px;
        }

        .tab {
            border: none;

            background: transparent;

            padding: 11px;

            border-radius: 8px;

            font-size: 13px;

            font-weight: 650;

            color: #6d7b74;

            cursor: pointer;

            transition: 0.25s;
        }

        .tab.active {
            background: white;

            color: #087f5b;

            box-shadow:
                0 2px 9px rgba(0,0,0,0.06);
        }

        /* ================================
           FORMS
        ================================= */

        .form {
            display: none;
        }

        .form.active {
            display: block;

            animation: fadeIn 0.3s ease;
        }

        @keyframes fadeIn {
            from {
                opacity: 0;

                transform: translateY(5px);
            }

            to {
                opacity: 1;

                transform: translateY(0);
            }
        }

        .form-row {
            display: grid;

            grid-template-columns: 1fr 1fr;

            gap: 13px;
        }

        .form-group {
            margin-bottom: 16px;
        }

        label {
            display: block;

            color: #34443c;

            font-size: 12px;

            font-weight: 650;

            margin-bottom: 7px;
        }

        .required {
            color: #e04747;
        }

        input,
        select {
            width: 100%;

            height: 45px;

            padding: 0 12px;

            border-radius: 9px;

            border: 1px solid #d7e3dd;

            outline: none;

            background: white;

            color: #27362f;

            font-size: 12px;

            transition: 0.2s;
        }

        textarea {
            width: 100%;

            min-height: 82px;

            resize: vertical;

            padding: 11px 12px;

            border-radius: 9px;

            border: 1px solid #d7e3dd;

            outline: none;

            background: white;

            color: #27362f;

            font-size: 12px;

            transition: 0.2s;
        }

        input:focus,
        select:focus,
        textarea:focus {
            border-color: #11a36e;

            box-shadow:
                0 0 0 3px rgba(17,163,110,0.10);
        }

        input::placeholder,
        textarea::placeholder {
            color: #a1ada7;
        }

        /* ================================
           PASSWORD
        ================================= */

        .password-box {
            position: relative;
        }

        .password-box input {
            padding-right: 43px;
        }

        .eye-btn {
            position: absolute;

            right: 11px;

            top: 50%;

            transform: translateY(-50%);

            border: none;

            background: transparent;

            cursor: pointer;

            color: #718078;

            font-size: 16px;
        }

        /* ================================
           PASSWORD STRENGTH
        ================================= */

        .password-strength {
            margin-top: 7px;

            height: 4px;

            background: #e7eeea;

            border-radius: 5px;

            overflow: hidden;
        }

        .strength-bar {
            height: 100%;

            width: 0%;

            background: #11a36e;

            transition: 0.3s;
        }

        .strength-text {
            font-size: 10px;

            margin-top: 5px;

            color: #7c8982;
        }

        /* ================================
           HEALTH SECTION
        ================================= */

        .health-section {
            margin: 22px 0;

            padding: 18px;

            border-radius: 14px;

            border: 1px solid #d9e9e1;

            background: #f8fcfa;
        }

        .health-title {
            display: flex;

            align-items: center;

            gap: 8px;

            margin-bottom: 5px;
        }

        .health-title h3 {
            color: #174e3c;

            font-size: 15px;
        }

        .health-title span {
            background: #e5f6ee;

            color: #087f5b;

            padding: 4px 8px;

            border-radius: 20px;

            font-size: 9px;

            font-weight: 700;
        }

        .health-description {
            color: #718078;

            font-size: 11px;

            line-height: 1.5;

            margin-bottom: 16px;
        }

        .conditional-health {
            display: none;
        }

        /* ================================
           CHECKBOX
        ================================= */

        .checkbox-row {
            display: flex;

            align-items: flex-start;

            gap: 8px;

            margin: 17px 0;
        }

        .checkbox-row input {
            width: 15px;
            height: 15px;

            margin-top: 2px;

            accent-color: #087f5b;
        }

        .checkbox-row label {
            margin: 0;

            color: #68766f;

            font-size: 11px;

            line-height: 1.5;

            font-weight: 400;
        }

        .checkbox-row a {
            color: #087f5b;

            text-decoration: none;

            font-weight: 650;
        }

        /* ================================
           LOGIN OPTIONS
        ================================= */

        .login-options {
            display: flex;

            align-items: center;

            justify-content: space-between;

            margin: 7px 0 20px;
        }

        .remember {
            display: flex;

            align-items: center;

            gap: 6px;
        }

        .remember input {
            width: 14px;
            height: 14px;

            accent-color: #087f5b;
        }

        .remember label {
            margin: 0;

            font-size: 11px;

            font-weight: 400;
        }

        .forgot {
            color: #087f5b;

            font-size: 11px;

            font-weight: 650;

            text-decoration: none;
        }

        /* ================================
           SUBMIT BUTTON
        ================================= */

        .submit-btn {
            width: 100%;

            height: 47px;

            border: none;

            border-radius: 10px;

            background:
                linear-gradient(
                    135deg,
                    #087f5b,
                    #10a66e
                );

            color: white;

            font-size: 13px;

            font-weight: 700;

            cursor: pointer;

            box-shadow:
                0 9px 20px rgba(8,127,91,0.18);

            transition: 0.25s;
        }

        .submit-btn:hover {
            transform: translateY(-2px);

            box-shadow:
                0 12px 25px rgba(8,127,91,0.25);
        }

        /* ================================
           DIVIDER
        ================================= */

        .divider {
            display: flex;

            align-items: center;

            gap: 11px;

            margin: 20px 0;

            color: #a0aaa5;

            font-size: 10px;
        }

        .divider::before,
        .divider::after {
            content: "";

            height: 1px;

            background: #e4ebe7;

            flex: 1;
        }

        /* ================================
           GOOGLE
        ================================= */

        .google-btn {
            width: 100%;

            height: 45px;

            border-radius: 9px;

            border: 1px solid #dce5e0;

            background: white;

            cursor: pointer;

            color: #35433c;

            font-size: 12px;

            font-weight: 600;

            transition: 0.2s;
        }

        .google-btn:hover {
            background: #f7faf8;

            border-color: #cbdad2;
        }

        /* ================================
           SECURITY NOTE
        ================================= */

        .security-note {
            margin-top: 16px;

            padding: 10px 12px;

            border-radius: 8px;

            background: #f3faf6;

            color: #597066;

            font-size: 10px;

            line-height: 1.5;

            text-align: center;
        }

        /* ================================
           TOAST
        ================================= */

        .toast {
            position: fixed;

            bottom: 25px;

            right: 25px;

            background: #143b2e;

            color: white;

            padding: 13px 17px;

            border-radius: 9px;

            font-size: 12px;

            box-shadow:
                0 10px 30px rgba(0,0,0,0.18);

            transform: translateY(100px);

            opacity: 0;

            transition: 0.3s;

            z-index: 1000;
        }

        .toast.show {
            transform: translateY(0);

            opacity: 1;
        }

        /* ================================
           RESPONSIVE
        ================================= */

        @media (max-width: 1000px) {

            .page {
                flex-direction: column;
            }

            .left-section {
                width: 100%;

                min-height: 450px;

                padding: 38px;
            }

            .right-section {
                width: 100%;

                min-height: auto;

                padding: 35px 25px;
            }

            .left-content h1 {
                font-size: 40px;
            }
        }

        @media (max-width: 600px) {

            .left-section {
                padding: 28px 20px;

                min-height: 510px;
            }

            .right-section {
                padding: 22px 14px;
            }

            .auth-card {
                padding: 22px;

                border-radius: 18px;
            }

            .left-content h1 {
                font-size: 34px;
            }

            .features {
                grid-template-columns: 1fr;
            }

            .form-row {
                grid-template-columns: 1fr;

                gap: 0;
            }

            .auth-heading h2 {
                font-size: 24px;
            }

            .brand-name {
                font-size: 22px;
            }
        }
    </style>
</head>

<body>

<div class="page">

    <!-- ==========================================
         LEFT SIDE
    =========================================== -->

    <section class="left-section">

        <!-- AERIQ LOGO -->

        <div class="brand">

            <div class="brand-icon">

                <!--
                    AeriQ air/wind symbol
                    based on the logo shown in the screenshot
                -->

                <svg
                    viewBox="0 0 40 40"
                    xmlns="http://www.w3.org/2000/svg"
                >

                    <!-- Top air line -->

                    <path
                        d="M8 14H24C27 14 29 12 29 10"
                        stroke="white"
                        stroke-width="2.5"
                        fill="none"
                        stroke-linecap="round"
                    />

                    <!-- Middle air line -->

                    <path
                        d="M8 19.5H29"
                        stroke="white"
                        stroke-width="2.5"
                        fill="none"
                        stroke-linecap="round"
                    />

                    <!-- Bottom air line -->

                    <path
                        d="M8 25H22C25 25 27 27 27 29"
                        stroke="white"
                        stroke-width="2.5"
                        fill="none"
                        stroke-linecap="round"
                    />

                    <!-- Air endpoints -->

                    <circle
                        cx="29"
                        cy="10"
                        r="1.6"
                        fill="white"
                    />

                    <circle
                        cx="27"
                        cy="29"
                        r="1.6"
                        fill="white"
                    />

                </svg>

            </div>


            <div class="brand-name">
                AeriQ
            </div>

        </div>


        <!-- LEFT CONTENT -->

        <div class="left-content">

            <h1>
                Your health,<br>
                <span>your information.</span>
            </h1>


            <p>
                Create your AeriQ account to securely manage
                your personal information and health details
                in one place.
            </p>


            <!-- FEATURES -->

            <div class="features">

                <div class="feature">

                    <div class="feature-icon">
                        🔒
                    </div>

                    <h3>
                        Secure
                    </h3>

                    <p>
                        Your information is designed
                        to remain protected.
                    </p>

                </div>


                <div class="feature">

                    <div class="feature-icon">
                        🛡️
                    </div>

                    <h3>
                        Private
                    </h3>

                    <p>
                        Your personal details stay
                        under your control.
                    </p>

                </div>


                <div class="feature">

                    <div class="feature-icon">
                        ⚡
                    </div>

                    <h3>
                        Simple
                    </h3>

                    <p>
                        A clean and easy-to-use
                        experience.
                    </p>

                </div>


                <div class="feature">

                    <div class="feature-icon">
                        💚
                    </div>

                    <h3>
                        Personalized
                    </h3>

                    <p>
                        Information can be tailored
                        to your needs.
                    </p>

                </div>

            </div>

        </div>


        <!-- COPYRIGHT -->

        <div class="copyright">
            © 2026 AeriQ. All rights reserved.
        </div>

    </section>


    <!-- ==========================================
         RIGHT SIDE
    =========================================== -->

    <section class="right-section">

        <div class="auth-wrapper">

            <!-- SECURITY BADGE -->

            <div class="top-bar">

                <div class="secure-badge">
                    🔐 Secure Registration
                </div>

            </div>


            <!-- AUTH CARD -->

            <div class="auth-card">

                <!-- HEADING -->

                <div class="auth-heading">

                    <h2 id="authTitle">
                        Welcome back
                    </h2>

                    <p id="authSubtitle">
                        Sign in to continue to your AeriQ account.
                    </p>

                </div>


                <!-- TABS -->

                <div class="tabs">

                    <button
                        class="tab active"
                        id="loginTab"
                        onclick="showLogin()"
                    >
                        Sign In
                    </button>


                    <button
                        class="tab"
                        id="registerTab"
                        onclick="showRegister()"
                    >
                        Create Account
                    </button>

                </div>


                <!-- ======================================
                     LOGIN FORM
                ======================================= -->

                <form
                    class="form active"
                    id="loginForm"
                    onsubmit="loginUser(event)"
                >

                    <!-- EMAIL -->

                    <div class="form-group">

                        <label>
                            Email Address
                            <span class="required">*</span>
                        </label>

                        <input
                            type="email"
                            id="loginEmail"
                            placeholder="Enter your email"
                            required
                        >

                    </div>


                    <!-- PASSWORD -->

                    <div class="form-group">

                        <label>
                            Password
                            <span class="required">*</span>
                        </label>


                        <div class="password-box">

                            <input
                                type="password"
                                id="loginPassword"
                                placeholder="Enter your password"
                                required
                            >


                            <button
                                type="button"
                                class="eye-btn"
                                onclick="togglePassword(
                                    'loginPassword',
                                    this
                                )"
                            >
                                👁
                            </button>

                        </div>

                    </div>


                    <!-- OPTIONS -->

                    <div class="login-options">

                        <div class="remember">

                            <input
                                type="checkbox"
                                id="remember"
                            >

                            <label for="remember">
                                Remember me
                            </label>

                        </div>


                        <a
                            href="#"
                            class="forgot"
                            onclick="forgotPassword(event)"
                        >
                            Forgot password?
                        </a>

                    </div>


                    <!-- LOGIN BUTTON -->

                    <button
                        class="submit-btn"
                        type="submit"
                    >
                        Sign In
                    </button>


                    <!-- DIVIDER -->

                    <div class="divider">
                        OR
                    </div>


                    <!-- GOOGLE -->

                    <button
                        type="button"
                        class="google-btn"
                        onclick="googleLogin()"
                    >
                        Continue with Google
                    </button>


                    <div class="security-note">
                        🔒 Your information is handled securely.
                    </div>

                </form>


                <!-- ======================================
                     REGISTER FORM
                ======================================= -->

                <form
                    class="form"
                    id="registerForm"
                    onsubmit="registerUser(event)"
                >

                    <!-- FIRST NAME + LAST NAME -->

                    <div class="form-row">

                        <div class="form-group">

                            <label>
                                First Name
                                <span class="required">*</span>
                            </label>

                            <input
                                type="text"
                                id="firstName"
                                placeholder="First name"
                                required
                            >

                        </div>


                        <div class="form-group">

                            <label>
                                Last Name
                                <span class="required">*</span>
                            </label>

                            <input
                                type="text"
                                id="lastName"
                                placeholder="Last name"
                                required
                            >

                        </div>

                    </div>


                    <!-- DOB + GENDER -->

                    <div class="form-row">

                        <div class="form-group">

                            <label>
                                Date of Birth
                                <span class="required">*</span>
                            </label>

                            <input
                                type="date"
                                id="dob"
                                required
                            >

                        </div>


                        <div class="form-group">

                            <label>
                                Gender
                                <span class="required">*</span>
                            </label>

                            <select
                                id="gender"
                                required
                            >

                                <option value="">
                                    Select gender
                                </option>

                                <option value="male">
                                    Male
                                </option>

                                <option value="female">
                                    Female
                                </option>

                                <option value="other">
                                    Other
                                </option>

                                <option value="prefer-not">
                                    Prefer not to say
                                </option>

                            </select>

                        </div>

                    </div>


                    <!-- EMAIL -->

                    <div class="form-group">

                        <label>
                            Email Address
                            <span class="required">*</span>
                        </label>

                        <input
                            type="email"
                            id="registerEmail"
                            placeholder="Enter your email address"
                            required
                        >

                    </div>


                    <!-- MOBILE -->

                    <div class="form-group">

                        <label>
                            Mobile Number
                            <span class="required">*</span>
                        </label>

                        <input
                            type="tel"
                            id="mobile"
                            placeholder="Enter your mobile number"
                            pattern="[0-9+\-\s]{10,15}"
                            required
                        >

                    </div>


                    <!-- CITY + COUNTRY -->

                    <div class="form-row">

                        <div class="form-group">

                            <label>
                                City
                                <span class="required">*</span>
                            </label>

                            <input
                                type="text"
                                id="city"
                                placeholder="Your city"
                                required
                            >

                        </div>


                        <div class="form-group">

                            <label>
                                Country
                                <span class="required">*</span>
                            </label>

                            <select
                                id="country"
                                required
                            >

                                <option value="">
                                    Select country
                                </option>

                                <option value="India">
                                    India
                                </option>

                                <option value="USA">
                                    United States
                                </option>

                                <option value="UK">
                                    United Kingdom
                                </option>

                                <option value="Canada">
                                    Canada
                                </option>

                                <option value="Australia">
                                    Australia
                                </option>

                                <option value="Other">
                                    Other
                                </option>

                            </select>

                        </div>

                    </div>


                    <!-- ACCOUNT TYPE -->

                    <div class="form-group">

                        <label>
                            Account Type
                            <span class="required">*</span>
                        </label>

                        <select
                            id="accountType"
                            required
                        >

                            <option value="">
                                Select account type
                            </option>

                            <option value="individual">
                                Individual
                            </option>

                            <option value="student">
                                Student
                            </option>

                            <option value="professional">
                                Professional
                            </option>

                            <option value="other">
                                Other
                            </option>

                        </select>

                    </div>


                    <!-- ======================================
                         HEALTH INFORMATION
                    ======================================= -->

                    <div class="health-section">

                        <div class="health-title">

                            <h3>
                                Health Information
                            </h3>

                            <span>
                                Required
                            </span>

                        </div>


                        <p class="health-description">
                            Please provide your current health
                            information so your AeriQ profile
                            can contain relevant details.
                        </p>


                        <!-- DISEASE QUESTION -->

                        <div class="form-group">

                            <label>
                                Do you have any existing medical
                                condition or disease?
                                <span class="required">*</span>
                            </label>


                            <select
                                id="hasDisease"
                                required
                                onchange="handleHealthChange()"
                            >

                                <option value="">
                                    Select an option
                                </option>

                                <option value="no">
                                    No
                                </option>

                                <option value="yes">
                                    Yes
                                </option>

                            </select>

                        </div>


                        <!-- EXTRA HEALTH DETAILS -->

                        <div
                            class="conditional-health"
                            id="conditionalHealth"
                        >

                            <!-- CONDITION -->

                            <div class="form-group">

                                <label>
                                    Medical Condition / Disease
                                    <span class="required">*</span>
                                </label>


                                <textarea
                                    id="conditions"
                                    placeholder="Please mention your medical condition(s)"
                                ></textarea>

                            </div>


                            <!-- ALLERGIES -->

                            <div class="form-group">

                                <label>
                                    Allergies
                                    <span class="required">*</span>
                                </label>


                                <textarea
                                    id="allergies"
                                    placeholder="Mention any known allergies"
                                ></textarea>

                            </div>


                            <!-- MEDICATIONS -->

                            <div class="form-group">

                                <label>
                                    Current Medications
                                    <span class="required">*</span>
                                </label>


                                <textarea
                                    id="medications"
                                    placeholder="Mention medicines you currently take"
                                ></textarea>

                            </div>

                        </div>

                    </div>


                    <!-- CREATE PASSWORD -->

                    <div class="form-group">

                        <label>
                            Create Password
                            <span class="required">*</span>
                        </label>


                        <div class="password-box">

                            <input
                                type="password"
                                id="registerPassword"
                                placeholder="Create a strong password"
                                required
                                oninput="checkPasswordStrength()"
                            >


                            <button
                                type="button"
                                class="eye-btn"
                                onclick="togglePassword(
                                    'registerPassword',
                                    this
                                )"
                            >
                                👁
                            </button>

                        </div>


                        <!-- STRENGTH BAR -->

                        <div class="password-strength">

                            <div
                                class="strength-bar"
                                id="strengthBar"
                            ></div>

                        </div>


                        <div
                            class="strength-text"
                            id="strengthText"
                        >
                            Password strength
                        </div>

                    </div>


                    <!-- CONFIRM PASSWORD -->

                    <div class="form-group">

                        <label>
                            Confirm Password
                            <span class="required">*</span>
                        </label>


                        <div class="password-box">

                            <input
                                type="password"
                                id="confirmPassword"
                                placeholder="Re-enter your password"
                                required
                            >


                            <button
                                type="button"
                                class="eye-btn"
                                onclick="togglePassword(
                                    'confirmPassword',
                                    this
                                )"
                            >
                                👁
                            </button>

                        </div>

                    </div>


                    <!-- TERMS -->

                    <div class="checkbox-row">

                        <input
                            type="checkbox"
                            id="terms"
                            required
                        >


                        <label for="terms">

                            I agree to the

                            <a href="#">
                                Terms of Service
                            </a>

                            and

                            <a href="#">
                                Privacy Policy
                            </a>.

                            <span class="required">*</span>

                        </label>

                    </div>


                    <!-- REGISTER BUTTON -->

                    <button
                        type="submit"
                        class="submit-btn"
                    >
                        Create AeriQ Account
                    </button>


                    <div class="security-note">

                        🔒 Your health information is sensitive
                        data. Only collect and store information
                        necessary for your application's purpose.

                    </div>

                </form>

            </div>

        </div>

    </section>

</div>


<!-- ==========================================
     TOAST MESSAGE
=========================================== -->

<div
    class="toast"
    id="toast"
></div>


<script>

    /* ==========================================
       SHOW LOGIN
    =========================================== */

    function showLogin() {

        document
            .getElementById("loginForm")
            .classList.add("active");


        document
            .getElementById("registerForm")
            .classList.remove("active");


        document
            .getElementById("loginTab")
            .classList.add("active");


        document
            .getElementById("registerTab")
            .classList.remove("active");


        document
            .getElementById("authTitle")
            .textContent = "Welcome back";


        document
            .getElementById("authSubtitle")
            .textContent =
            "Sign in to continue to your AeriQ account.";
    }


    /* ==========================================
       SHOW REGISTER
    =========================================== */

    function showRegister() {

        document
            .getElementById("registerForm")
            .classList.add("active");


        document
            .getElementById("loginForm")
            .classList.remove("active");


        document
            .getElementById("registerTab")
            .classList.add("active");


        document
            .getElementById("loginTab")
            .classList.remove("active");


        document
            .getElementById("authTitle")
            .textContent = "Create your account";


        document
            .getElementById("authSubtitle")
            .textContent =
            "Enter your details to get started with AeriQ.";
    }


    /* ==========================================
       PASSWORD VISIBILITY
    =========================================== */

    function togglePassword(inputId, button) {

        const input =
            document.getElementById(inputId);


        if (input.type === "password") {

            input.type = "text";

            button.textContent = "🙈";

        } else {

            input.type = "password";

            button.textContent = "👁";
        }
    }


    /* ==========================================
       PASSWORD STRENGTH
    =========================================== */

    function checkPasswordStrength() {

        const password =
            document
                .getElementById("registerPassword")
                .value;


        const bar =
            document.getElementById("strengthBar");


        const text =
            document.getElementById("strengthText");


        let strength = 0;


        if (password.length >= 8) {
            strength++;
        }


        if (/[A-Z]/.test(password)) {
            strength++;
        }


        if (/[0-9]/.test(password)) {
            strength++;
        }


        if (/[^A-Za-z0-9]/.test(password)) {
            strength++;
        }


        if (password.length === 0) {

            bar.style.width = "0%";

            text.textContent =
                "Password strength";

        } else if (strength <= 1) {

            bar.style.width = "25%";

            text.textContent =
                "Weak password";

        } else if (strength === 2) {

            bar.style.width = "50%";

            text.textContent =
                "Fair password";

        } else if (strength === 3) {

            bar.style.width = "75%";

            text.textContent =
                "Good password";

        } else {

            bar.style.width = "100%";

            text.textContent =
                "Strong password";
        }
    }


    /* ==========================================
       HEALTH INFORMATION
    =========================================== */

    function handleHealthChange() {

        const disease =
            document
                .getElementById("hasDisease")
                .value;


        const healthDetails =
            document
                .getElementById("conditionalHealth");


        const conditions =
            document
                .getElementById("conditions");


        const allergies =
            document
                .getElementById("allergies");


        const medications =
            document
                .getElementById("medications");


        if (disease === "yes") {

            healthDetails.style.display = "block";

            conditions.required = true;

            allergies.required = true;

            medications.required = true;

        } else {

            healthDetails.style.display = "none";

            conditions.required = false;

            allergies.required = false;

            medications.required = false;

            conditions.value = "";

            allergies.value = "";

            medications.value = "";
        }
    }


    /* ==========================================
       LOGIN
    =========================================== */

    function loginUser(event) {

        event.preventDefault();


        const email =
            document
                .getElementById("loginEmail")
                .value;


        showToast(
            "Welcome back! Login request submitted for " +
            email
        );
    }


    /* ==========================================
       REGISTER
    =========================================== */

    function registerUser(event) {

        event.preventDefault();


        const password =
            document
                .getElementById("registerPassword")
                .value;


        const confirmPassword =
            document
                .getElementById("confirmPassword")
                .value;


        const healthAnswer =
            document
                .getElementById("hasDisease")
                .value;


        /* PASSWORD CHECK */

        if (password !== confirmPassword) {

            showToast(
                "Passwords do not match."
            );

            return;
        }


        /* HEALTH CHECK */

        if (healthAnswer === "") {

            showToast(
                "Please provide your health information."
            );

            return;
        }


        /* ADDITIONAL HEALTH DETAILS */

        if (healthAnswer === "yes") {

            const conditions =
                document
                    .getElementById("conditions")
                    .value
                    .trim();


            const allergies =
                document
                    .getElementById("allergies")
                    .value
                    .trim();


            const medications =
                document
                    .getElementById("medications")
                    .value
                    .trim();


            if (
                conditions === "" ||
                allergies === "" ||
                medications === ""
            ) {

                showToast(
                    "Please complete all required health information."
                );

                return;
            }
        }


        showToast(
            "AeriQ account created successfully!"
        );
    }


    /* ==========================================
       GOOGLE LOGIN
    =========================================== */

    function googleLogin() {

        showToast(
            "Google sign-in will be connected to your backend."
        );
    }


    /* ==========================================
       FORGOT PASSWORD
    =========================================== */

    function forgotPassword(event) {

        event.preventDefault();

        showToast(
            "Password reset will be connected to your backend."
        );
    }


    /* ==========================================
       TOAST
    =========================================== */

    function showToast(message) {

        const toast =
            document.getElementById("toast");


        toast.textContent = message;


        toast.classList.add("show");


        setTimeout(function() {

            toast.classList.remove("show");

        }, 3500);
    }

</script>

</body>
</html>