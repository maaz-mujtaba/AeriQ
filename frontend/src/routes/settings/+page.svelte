<script>
    import { loggedIn, login } from '$lib/stores/authStore.js';
    import { goto } from '$app/navigation';

/* =========================
       TAB SWITCHING
    ========================== */

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

        document.getElementById("authTitle").textContent =
            "Welcome back";

        document.getElementById("authSubtitle").textContent =
            "Sign in to continue to your AeriQ account.";
    }


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

        document.getElementById("authTitle").textContent =
            "Create your account";

        document.getElementById("authSubtitle").textContent =
            "Enter your details to get started with AeriQ.";
    }


    /* =========================
       PASSWORD VISIBILITY
    ========================== */

    function togglePassword(inputId, button) {

        const input = document.getElementById(inputId);

        if (input.type === "password") {

            input.type = "text";
            button.textContent = "🙈";

        } else {

            input.type = "password";
            button.textContent = "👁";

        }
    }


    /* =========================
       PASSWORD STRENGTH
    ========================== */

    function checkPasswordStrength() {

        const password =
            document.getElementById("registerPassword").value;

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
            text.textContent = "Password strength";

        } else if (strength <= 1) {

            bar.style.width = "25%";
            text.textContent = "Weak password";

        } else if (strength === 2) {

            bar.style.width = "50%";
            text.textContent = "Fair password";

        } else if (strength === 3) {

            bar.style.width = "75%";
            text.textContent = "Good password";

        } else {

            bar.style.width = "100%";
            text.textContent = "Strong password";
        }
    }


    /* =========================
       HEALTH INFORMATION
    ========================== */

    function handleHealthChange() {

        const disease =
            document.getElementById("hasDisease").value;

        const healthDetails =
            document.getElementById("conditionalHealth");

        const conditions =
            document.getElementById("conditions");

        const allergies =
            document.getElementById("allergies");

        const medications =
            document.getElementById("medications");


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


    /* =========================
       LOGIN
    ========================== */

    function loginUser(event) {
    event.preventDefault();

    const email = document.getElementById("loginEmail").value.trim();
    const password = document.getElementById("loginPassword").value;

    if (!email || !password) {
        showToast("Please enter your email and password.");
        return;
    }

    login();

    showToast("Welcome back! Login successful.");

    setTimeout(() => {
        goto("/");
    }, 500);
}


    /* =========================
       REGISTER
    ========================== */

    function registerUser(event) {

        event.preventDefault();

        const password =
            document.getElementById("registerPassword").value;

        const confirmPassword =
            document.getElementById("confirmPassword").value;

        const healthAnswer =
            document.getElementById("hasDisease").value;


        /* Password check */

        if (password !== confirmPassword) {

            showToast(
                "Passwords do not match."
            );

            return;
        }


        /* Health information check */

        if (healthAnswer === "") {

            showToast(
                "Please provide your health information."
            );

            return;
        }


        /* Disease details check */

        if (healthAnswer === "yes") {

            const conditions =
                document.getElementById("conditions").value.trim();

            const allergies =
                document.getElementById("allergies").value.trim();

            const medications =
                document.getElementById("medications").value.trim();


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


                login();

        showToast(
            "AeriQ account created successfully!"
        );

        setTimeout(() => {
            goto("/");
        }, 800);
    }


    /*GOOGLE LOGIN */

    function googleLogin() {

        showToast(
            "Google sign-in will be connected to your backend."
        );
    }


    /*TOAST*/

    function showToast(message) {

        const toast =
            document.getElementById("toast");

        toast.textContent = message;

        toast.classList.add("show");

        setTimeout(() => {

            toast.classList.remove("show");

        }, 3500);
    }
</script>

<svelte:head>
    <title>AeriQ - Sign In / Register</title>
    <meta name="description" content="Sign in or create an AeriQ account." />
</svelte:head>

{#if !$loggedIn}
    <div class="auth-shell">
<div class="auth-page">

    <!-- =========================
         LEFT SIDE
    ========================== -->

    <section class="left-section">

        <div class="brand">
            <div class="brand-logo">A</div>
            <div class="brand-name">AeriQ</div>
        </div>

        <div class="left-content">

            <h1>
                Your health,<br>
                <span>your information.</span>
            </h1>

            <p>
                Create your AeriQ account to securely manage your
                personal information and health details in one place.
            </p>

            <div class="features">

                <div class="feature">
                    <div class="feature-icon">🔒</div>
                    <h3>Secure</h3>
                    <p>Your information is designed to remain protected.</p>
                </div>

                <div class="feature">
                    <div class="feature-icon">🛡️</div>
                    <h3>Private</h3>
                    <p>Your personal details stay under your control.</p>
                </div>

                <div class="feature">
                    <div class="feature-icon">⚡</div>
                    <h3>Simple</h3>
                    <p>A clean and easy-to-use experience.</p>
                </div>

                <div class="feature">
                    <div class="feature-icon">💚</div>
                    <h3>Personalized</h3>
                    <p>Information can be tailored to your needs.</p>
                </div>

            </div>

        </div>

        <div class="copyright">
            © 2026 AeriQ. All rights reserved.
        </div>

    </section>


    <!-- =========================
         RIGHT SIDE
    ========================== -->

    <section class="right-section">

        <div class="auth-wrapper">

            <div class="top-bar">
                <div class="secure-badge">
                    🔐 Secure Registration
                </div>
            </div>

            <div class="auth-card">

                <div class="auth-heading">
                    <h2 id="authTitle">Welcome back</h2>
                    <p id="authSubtitle">
                        Sign in to continue to your AeriQ account.
                    </p>
                </div>


                <!-- =========================
                     TABS
                ========================== -->

                <div class="tabs">

                    <button
                        class="tab active"
                        id="loginTab"
                        onclick={showLogin}>
                        Sign In
                    </button>

                    <button
                        class="tab"
                        id="registerTab"
                        onclick={showRegister}>
                        Create Account
                    </button>

                </div>


                <!-- =========================
                     LOGIN FORM
                ========================== -->

                <form
                    class="form active"
                    id="loginForm"
                    onsubmit={loginUser}
                >

                    <div class="form-group">

                        <label>
                            Email Address <span class="required">*</span>
                        </label>

                        <input
                            type="email"
                            id="loginEmail"
                            placeholder="Enter your email"
                            required
                        >

                    </div>


                    <div class="form-group">

                        <label>
                            Password <span class="required">*</span>
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
                                onclick={(event) => togglePassword('loginPassword', event.currentTarget)}
                            >
                                👁
                            </button>

                        </div>

                    </div>


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

                        <a href="#" class="forgot">
                            Forgot password?
                        </a>

                    </div>


                    <button class="submit-btn" type="submit">
                        Sign In
                    </button>


                    <div class="divider">
                        OR
                    </div>


                    <button
                        type="button"
                        class="google-btn"
                        onclick={googleLogin}
                    >
                        Continue with Google
                    </button>


                    <div class="security-note">
                        🔒 Your information is handled securely.
                    </div>

                </form>


                <!-- =========================
                     REGISTER FORM
                ========================== -->

                <form
                    class="form"
                    id="registerForm"
                    onsubmit={registerUser}
                >

                    <!-- NAME -->

                    <div class="form-row">

                        <div class="form-group">

                            <label>
                                First Name <span class="required">*</span>
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
                                Last Name <span class="required">*</span>
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
                                Date of Birth <span class="required">*</span>
                            </label>

                            <input
                                type="date"
                                id="dob"
                                required
                            >

                        </div>


                        <div class="form-group">

                            <label>
                                Gender <span class="required">*</span>
                            </label>

                            <select id="gender" required>

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
                            Email Address <span class="required">*</span>
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
                            Mobile Number <span class="required">*</span>
                        </label>

                        <input
                            type="tel"
                            id="mobile"
                            placeholder="Enter your mobile number"
                            pattern="[0-9]{10}"
                            required
                        >

                    </div>


                    <!-- LOCATION -->

                    <div class="form-row">

                        <div class="form-group">

                            <label>
                                City <span class="required">*</span>
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
                                Country <span class="required">*</span>
                            </label>

                            <select id="country" required>

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
                            Account Type <span class="required">*</span>
                        </label>

                        <select id="accountType" required>

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


                    <!-- =========================
                         HEALTH INFORMATION
                    ========================== -->

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
                            Please provide your current health information
                            so your AeriQ profile can contain relevant details.
                        </p>


                        <!-- DISEASE QUESTION -->

                        <div class="form-group">

                            <label>
                                Do you have any existing medical condition
                                or disease?
                                <span class="required">*</span>
                            </label>

                            <select
                                id="hasDisease"
                                required
                                onchange={handleHealthChange}
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


                        <!-- CONDITIONAL HEALTH INFORMATION -->

                        <div
                            class="conditional-health"
                            id="conditionalHealth"
                        >

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


                    <!-- PASSWORD -->

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
                                oninput={checkPasswordStrength}
                            >

                            <button
                                type="button"
                                class="eye-btn"
                                onclick={(event) => togglePassword('registerPassword', event.currentTarget)}
                            >
                                👁
                            </button>

                        </div>

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
                                onclick={(event) => togglePassword('confirmPassword', event.currentTarget)}
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


                    <!-- SUBMIT -->

                    <button
                        type="submit"
                        class="submit-btn"
                    >
                        Create AeriQ Account
                    </button>


                    <div class="security-note">
                        🔒 Your health information is sensitive data.
                        Only collect and store information that is necessary
                        for your application's purpose.
                    </div>

                </form>

            </div>

        </div>

    </section>

</div>


<!-- TOAST -->

<div
    class="toast"
    id="toast"
></div>
    </div>
{:else}
    <div class="space-y-6">
        <div class="space-y-1">
            <div class="flex items-center gap-2 text-xs font-semibold text-zinc-400 dark:text-zinc-500 uppercase tracking-wider">
                <span>App</span><span>/</span><span class="text-emerald-500 dark:text-emerald-400">Settings</span>
            </div>
            <h1 class="text-3xl font-extrabold tracking-tight text-zinc-900 dark:text-white">Settings</h1>
            <p class="text-sm text-zinc-500 dark:text-zinc-400">Configure account preferences, email routing, API keys, and dark/light system sync.</p>
        </div>
        <div class="bg-white dark:bg-zinc-900 border border-zinc-200/80 dark:border-zinc-800/80 rounded-2xl p-8 shadow-sm flex flex-col items-center justify-center text-center min-h-[400px] gap-4">
            <div class="h-16 w-16 rounded-2xl bg-emerald-50 dark:bg-emerald-950/30 text-emerald-500 flex items-center justify-center">
                <span class="text-3xl">⚙</span>
            </div>
            <h2 class="text-xl font-bold text-zinc-900 dark:text-white">Settings Panel Under Development</h2>
            <p class="text-sm text-zinc-500 dark:text-zinc-400 max-w-md">Manage notification alerts, configure vulnerable group metrics, and modify geolocation preferences or Celsius/Fahrenheit units.</p>
        </div>
    </div>
{/if}

<style>
.auth-page,
        .auth-page * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: "Inter", "Segoe UI", Arial, sans-serif;
        }

        .auth-page {
            min-height: 100vh;
            background: #f5faf7;
            color: #17231d;
        }

        /* =========================
           MAIN CONTAINER
        ========================= */

        .auth-page {
            min-height: 100vh;
            display: flex;
        }

        /* =========================
           LEFT SECTION
        ========================= */

        .left-section {
            width: 46%;
            background: linear-gradient(145deg, #064e3b, #087f5b, #12a66f);
            color: white;
            padding: 55px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            position: relative;
            overflow: hidden;
        }

        .left-section::before {
            content: "";
            position: absolute;
            width: 400px;
            height: 400px;
            border-radius: 50%;
            background: rgba(255,255,255,0.07);
            top: -130px;
            right: -130px;
        }

        .left-section::after {
            content: "";
            position: absolute;
            width: 300px;
            height: 300px;
            border-radius: 50%;
            background: rgba(255,255,255,0.06);
            bottom: -120px;
            left: -100px;
        }

        /* =========================
           BRAND
        ========================= */

        .brand {
            display: flex;
            align-items: center;
            gap: 12px;
            position: relative;
            z-index: 2;
        }

        .brand-logo {
            width: 45px;
            height: 45px;
            border-radius: 13px;
            background: white;
            color: #087f5b;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 22px;
            font-weight: 800;
            box-shadow: 0 8px 20px rgba(0,0,0,0.12);
        }

        .brand-name {
            font-size: 27px;
            font-weight: 800;
            letter-spacing: -0.5px;
        }

        /* =========================
           LEFT CONTENT
        ========================= */

        .left-content {
            position: relative;
            z-index: 2;
            max-width: 540px;
        }

        .left-content h1 {
            font-size: 48px;
            line-height: 1.1;
            margin-bottom: 22px;
            letter-spacing: -1.5px;
        }

        .left-content h1 span {
            color: #b8f5dc;
        }

        .left-content p {
            font-size: 17px;
            line-height: 1.7;
            color: #d9f8eb;
            margin-bottom: 35px;
        }

        /* =========================
           FEATURES
        ========================= */

        .features {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
        }

        .feature {
            padding: 18px;
            border: 1px solid rgba(255,255,255,0.15);
            background: rgba(255,255,255,0.08);
            backdrop-filter: blur(8px);
            border-radius: 15px;
        }

        .feature-icon {
            width: 38px;
            height: 38px;
            background: rgba(255,255,255,0.16);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 12px;
            font-size: 18px;
        }

        .feature h3 {
            font-size: 15px;
            margin-bottom: 5px;
        }

        .feature p {
            font-size: 12px;
            margin: 0;
            line-height: 1.5;
            color: #d7f8e9;
        }

        .copyright {
            position: relative;
            z-index: 2;
            color: #c9efdf;
            font-size: 12px;
        }

        /* =========================
           RIGHT SECTION
        ========================= */

        .right-section {
            width: 54%;
            background: #ffffff;
            padding: 35px 60px;
            display: flex;
            justify-content: center;
            align-items: flex-start;
            overflow-y: auto;
        }

        .auth-wrapper {
            width: 100%;
            max-width: 540px;
        }

        /* =========================
           TOP BAR
        ========================= */

        .top-bar {
            display: flex;
            justify-content: flex-end;
            margin-bottom: 20px;
        }

        .secure-badge {
            display: flex;
            align-items: center;
            gap: 7px;
            padding: 8px 13px;
            background: #effaf5;
            border: 1px solid #d8f2e5;
            color: #087f5b;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }

        /* =========================
           AUTH CARD
        ========================= */

        .auth-card {
            border: 1px solid #e3ece7;
            border-radius: 24px;
            padding: 34px;
            box-shadow: 0 18px 55px rgba(19, 67, 49, 0.08);
        }

        .auth-heading {
            margin-bottom: 25px;
        }

        .auth-heading h2 {
            font-size: 29px;
            margin-bottom: 8px;
            color: #15231c;
        }

        .auth-heading p {
            font-size: 14px;
            color: #718078;
        }

        /* =========================
           TABS
        ========================= */

        .tabs {
            display: grid;
            grid-template-columns: 1fr 1fr;
            background: #f0f6f3;
            border-radius: 12px;
            padding: 4px;
            margin-bottom: 27px;
        }

        .tab {
            border: none;
            background: transparent;
            padding: 12px;
            border-radius: 9px;
            font-size: 14px;
            font-weight: 600;
            color: #6d7b74;
            cursor: pointer;
            transition: 0.25s;
        }

        .tab.active {
            background: white;
            color: #087f5b;
            box-shadow: 0 2px 10px rgba(0,0,0,0.06);
        }

        /* =========================
           FORMS
        ========================= */

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
            gap: 14px;
        }

        .form-group {
            margin-bottom: 17px;
        }

        .auth-page label {
            display: block;
            font-size: 13px;
            font-weight: 650;
            color: #34443c;
            margin-bottom: 7px;
        }

        .required {
            color: #e04747;
        }

        .auth-page input,
        .auth-page select {
            width: 100%;
            height: 46px;
            border: 1px solid #d7e3dd;
            border-radius: 10px;
            padding: 0 13px;
            outline: none;
            font-size: 13px;
            color: #27362f;
            background: #ffffff;
            transition: 0.2s;
        }

        .auth-page textarea {
            width: 100%;
            min-height: 85px;
            resize: vertical;
            border: 1px solid #d7e3dd;
            border-radius: 10px;
            padding: 12px 13px;
            outline: none;
            font-size: 13px;
            color: #27362f;
            background: #ffffff;
            transition: 0.2s;
        }

        .auth-page input:focus,
        .auth-page select:focus,
        .auth-page textarea:focus {
            border-color: #11a36e;
            box-shadow: 0 0 0 3px rgba(17,163,110,0.10);
        }

        .auth-page input::placeholder,
        .auth-page textarea::placeholder {
            color: #a1ada7;
        }

        /* =========================
           PASSWORD
        ========================= */

        .password-box {
            position: relative;
        }

        .password-box input {
            padding-right: 45px;
        }

        .eye-btn {
            position: absolute;
            right: 12px;
            top: 50%;
            transform: translateY(-50%);
            border: none;
            background: transparent;
            cursor: pointer;
            color: #718078;
            font-size: 17px;
        }

        /* =========================
           PASSWORD STRENGTH
        ========================= */

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
            transition: 0.3s;
        }

        .strength-text {
            font-size: 11px;
            margin-top: 5px;
            color: #7c8982;
        }

        /* =========================
           HEALTH SECTION
        ========================= */

        .health-section {
            margin: 23px 0;
            padding: 19px;
            border: 1px solid #d9e9e1;
            background: #f8fcfa;
            border-radius: 15px;
        }

        .health-title {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 4px;
        }

        .health-title h3 {
            font-size: 16px;
            color: #174e3c;
        }

        .health-title span {
            font-size: 11px;
            background: #e5f6ee;
            color: #087f5b;
            padding: 4px 8px;
            border-radius: 20px;
            font-weight: 600;
        }

        .health-description {
            font-size: 12px;
            color: #718078;
            line-height: 1.5;
            margin-bottom: 18px;
        }

        .conditional-health {
            display: none;
        }

        /* =========================
           CHECKBOX
        ========================= */

        .checkbox-row {
            display: flex;
            align-items: flex-start;
            gap: 9px;
            margin: 18px 0;
        }

        .checkbox-row input {
            width: 16px;
            height: 16px;
            margin-top: 2px;
            accent-color: #087f5b;
        }

        .checkbox-row label {
            font-size: 12px;
            line-height: 1.5;
            margin: 0;
            font-weight: 400;
            color: #68766f;
        }

        .checkbox-row a {
            color: #087f5b;
            text-decoration: none;
            font-weight: 600;
        }

        /* =========================
           FORGOT / REMEMBER
        ========================= */

        .login-options {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 8px 0 21px;
        }

        .remember {
            display: flex;
            align-items: center;
            gap: 7px;
        }

        .remember input {
            width: 15px;
            height: 15px;
            accent-color: #087f5b;
        }

        .remember label {
            margin: 0;
            font-size: 12px;
            font-weight: 400;
        }

        .forgot {
            font-size: 12px;
            color: #087f5b;
            font-weight: 600;
            text-decoration: none;
        }

        /* =========================
           BUTTON
        ========================= */

        .submit-btn {
            width: 100%;
            height: 48px;
            border: none;
            border-radius: 11px;
            background: linear-gradient(135deg, #087f5b, #10a66e);
            color: white;
            font-size: 14px;
            font-weight: 700;
            cursor: pointer;
            box-shadow: 0 9px 20px rgba(8,127,91,0.18);
            transition: 0.25s;
        }

        .submit-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 25px rgba(8,127,91,0.25);
        }

        /* =========================
           DIVIDER
        ========================= */

        .divider {
            display: flex;
            align-items: center;
            gap: 12px;
            margin: 22px 0;
            color: #a0aaa5;
            font-size: 11px;
        }

        .divider::before,
        .divider::after {
            content: "";
            height: 1px;
            background: #e4ebe7;
            flex: 1;
        }

        /* =========================
           GOOGLE BUTTON
        ========================= */

        .google-btn {
            width: 100%;
            height: 46px;
            border: 1px solid #dce5e0;
            border-radius: 10px;
            background: white;
            cursor: pointer;
            font-size: 13px;
            font-weight: 600;
            color: #35433c;
            transition: 0.2s;
        }

        .google-btn:hover {
            background: #f7faf8;
            border-color: #cbdad2;
        }

        /* =========================
           SECURITY NOTE
        ========================= */

        .security-note {
            margin-top: 18px;
            padding: 11px 13px;
            border-radius: 9px;
            background: #f3faf6;
            color: #597066;
            font-size: 11px;
            line-height: 1.5;
            text-align: center;
        }

        /* =========================
           TOAST
        ========================= */

        .toast {
            position: fixed;
            bottom: 25px;
            right: 25px;
            background: #143b2e;
            color: white;
            padding: 14px 18px;
            border-radius: 10px;
            font-size: 13px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.18);
            transform: translateY(100px);
            opacity: 0;
            transition: 0.3s;
            z-index: 1000;
        }

        .toast.show {
            transform: translateY(0);
            opacity: 1;
        }

        /* =========================
           RESPONSIVE
        ========================= */

        @media (max-width: 1000px) {
            .auth-page {
                flex-direction: column;
            }

            .left-section {
                width: 100%;
                min-height: 420px;
                padding: 40px;
            }

            .right-section {
                width: 100%;
                padding: 40px 25px;
            }

            .left-content h1 {
                font-size: 40px;
            }
        }

        @media (max-width: 600px) {
            .left-section {
                padding: 30px 22px;
                min-height: 460px;
            }

            .right-section {
                padding: 25px 15px;
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
                font-size: 25px;
            }
        }

    .auth-shell {
        width: 100%;
        min-height: calc(100vh - 7rem);
    }
</style>
