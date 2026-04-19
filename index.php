<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="PlanX - Intelligent Exam Scheduling System powered by AI">
    <title>PlanX | Intelligent Scheduling</title>

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;700;900&family=Tajawal:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

    <!-- Libraries -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollToPlugin.min.js"></script>

    <style>
        /* ===== VARIABLES ===== */
        :root {
            --bg-core: #07090f;
            --bg-secondary: #0d1526;
            --primary: #8b5cf6;
            --primary-light: #a78bfa;
            --primary-dark: #6d28d9;
            --primary-glow: rgba(139, 92, 246, 0.5);
            --accent: #06b6d4;
            --accent-light: #22d3ee;
            --accent-glow: rgba(6, 182, 212, 0.5);
            --text-main: #f8fafc;
            --text-muted: #cbd5e1;
            --text-light: #94a3b8;
            --border-light: rgba(139, 92, 246, 0.25);
            --font-en: 'Outfit', sans-serif;
            --font-ar: 'Tajawal', sans-serif;
            --ease-out: cubic-bezier(0.22, 1, 0.36, 1);
            --ease-bounce: cubic-bezier(0.34, 1.56, 0.64, 1);
        }

        * { margin: 0; padding: 0; box-sizing: border-box; outline: none; }
        html { scroll-behavior: smooth; scroll-padding-top: 100px; }

        body {
            background-color: var(--bg-core);
            color: var(--text-main);
            font-family: var(--font-en);
            overflow-x: hidden;
            line-height: 1.7;
        }

        body::before {
            content: '';
            position: fixed;
            inset: 0;
            background:
                radial-gradient(ellipse 60% 50% at 15% 20%, rgba(139,92,246,0.07) 0%, transparent 60%),
                radial-gradient(ellipse 50% 40% at 85% 75%, rgba(6,182,212,0.07) 0%, transparent 60%);
            pointer-events: none;
            z-index: 0;
        }

        /* ===== PRELOADER ===== */
        .preloader {
            position: fixed;
            inset: 0;
            background: var(--bg-core);
            z-index: 9999;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            gap: 40px;
            transition: opacity 0.8s ease, visibility 0.8s ease;
        }
        .preloader.hidden {
            opacity: 0;
            visibility: hidden;
            pointer-events: none;
        }

        /* Fixed 3D cube using proper perspective */
        .loader-cube-scene {
            width: 100px;
            height: 100px;
            perspective: 400px;
        }
        .loader-cube {
            width: 100%;
            height: 100%;
            position: relative;
            transform-style: preserve-3d;
            animation: cubeSpin 3s linear infinite;
        }
        @keyframes cubeSpin {
            from { transform: rotateX(20deg) rotateY(0deg); }
            to   { transform: rotateX(20deg) rotateY(360deg); }
        }
        .loader-face {
            position: absolute;
            width: 100px;
            height: 100px;
            border-radius: 16px;
            border: 1px solid rgba(255,255,255,0.15);
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .loader-face.front  { background: linear-gradient(135deg,rgba(139,92,246,0.9),rgba(6,182,212,0.7)); transform: translateZ(50px); }
        .loader-face.back   { background: linear-gradient(135deg,rgba(6,182,212,0.9),rgba(139,92,246,0.7)); transform: rotateY(180deg) translateZ(50px); }
        .loader-face.left   { background: linear-gradient(135deg,rgba(139,92,246,0.7),rgba(109,40,217,0.9)); transform: rotateY(-90deg) translateZ(50px); }
        .loader-face.right  { background: linear-gradient(135deg,rgba(6,182,212,0.7),rgba(8,145,178,0.9)); transform: rotateY(90deg) translateZ(50px); }
        .loader-face.top    { background: linear-gradient(135deg,rgba(167,139,250,0.8),rgba(34,211,238,0.8)); transform: rotateX(90deg) translateZ(50px); }
        .loader-face.bottom { background: linear-gradient(135deg,rgba(109,40,217,0.8),rgba(8,145,178,0.8)); transform: rotateX(-90deg) translateZ(50px); }

        .loader-brand {
            font-size: 2.2rem;
            font-weight: 900;
            letter-spacing: 0.15em;
            background: linear-gradient(135deg, var(--primary-light), var(--accent-light));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .progress-container {
            width: 260px;
            height: 3px;
            background: rgba(255,255,255,0.08);
            border-radius: 10px;
            overflow: hidden;
        }
        .progress-bar {
            height: 100%;
            background: linear-gradient(90deg, var(--primary), var(--accent));
            box-shadow: 0 0 12px var(--primary-glow);
            width: 0%;
            animation: loadProgress 2s var(--ease-out) forwards;
        }
        @keyframes loadProgress { to { width: 100%; } }

        /* ===== NAVBAR ===== */
        .navbar {
            position: fixed;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            width: min(90%, 1400px);
            padding: 14px 28px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(7, 9, 15, 0.75);
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            border: 1px solid var(--border-light);
            border-radius: 100px;
            z-index: 1000;
            transition: all 0.4s var(--ease-out);
            box-shadow: 0 8px 32px rgba(0,0,0,0.4);
        }
        .navbar.scrolled {
            top: 8px;
            background: rgba(7,9,15,0.92);
            border-color: rgba(139,92,246,0.5);
            box-shadow: 0 12px 40px -8px var(--primary-glow), 0 0 0 1px rgba(139,92,246,0.1);
        }

        .brand {
            font-size: 1.7rem;
            font-weight: 900;
            color: #fff;
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 10px;
            letter-spacing: 0.02em;
        }
        .brand i {
            color: var(--primary-light);
            filter: drop-shadow(0 0 12px var(--primary-glow));
            animation: iconFloat 3s ease-in-out infinite;
        }
        @keyframes iconFloat {
            0%,100% { transform: translateY(0) rotate(0deg); }
            50% { transform: translateY(-4px) rotate(8deg); }
        }

        .nav-links {
            display: flex;
            gap: 32px;
            align-items: center;
        }
        .nav-item {
            color: var(--text-muted);
            text-decoration: none;
            font-weight: 500;
            font-size: 0.95rem;
            position: relative;
            transition: color 0.3s;
            padding: 4px 0;
        }
        .nav-item::after {
            content: '';
            position: absolute;
            bottom: -3px;
            left: 0;
            width: 0;
            height: 2px;
            background: linear-gradient(90deg, var(--primary), var(--accent));
            transition: width 0.3s var(--ease-bounce);
            border-radius: 2px;
        }
        .nav-item:hover { color: #fff; }
        .nav-item:hover::after,
        .nav-item.active::after { width: 100%; }
        .nav-item.active { color: #fff; }

        .lang-toggle {
            background: rgba(139,92,246,0.1);
            border: 1px solid var(--border-light);
            color: var(--text-main);
            padding: 10px 26px;
            border-radius: 50px;
            cursor: pointer;
            font-weight: 700;
            font-size: 0.9rem;
            transition: all 0.35s var(--ease-bounce);
            display: flex;
            gap: 8px;
            align-items: center;
            font-family: var(--font-en);
        }
        .lang-toggle:hover {
            border-color: var(--primary);
            background: rgba(139,92,246,0.2);
            transform: translateY(-2px);
            box-shadow: 0 8px 20px -4px var(--primary-glow);
        }

        .mobile-toggle {
            display: none;
            background: rgba(139,92,246,0.1);
            border: 1px solid var(--border-light);
            color: #fff;
            width: 42px;
            height: 42px;
            border-radius: 50%;
            cursor: pointer;
            font-size: 1.1rem;
            align-items: center;
            justify-content: center;
            transition: all 0.3s;
        }
        .mobile-toggle:hover {
            background: var(--primary);
            border-color: var(--primary);
        }

        /* ===== HERO ===== */
        .hero {
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            padding: 160px 20px 100px;
            position: relative;
            overflow: hidden;
        }
        #hero-3d-canvas {
            position: absolute;
            inset: 0;
            z-index: 0;
            pointer-events: none;
        }
        .hero-content {
            position: relative;
            z-index: 2;
            max-width: 1100px;
            opacity: 0;
            transform: translateY(30px);
        }
        .hero-content.visible {
            animation: heroReveal 1s var(--ease-out) forwards;
        }
        @keyframes heroReveal {
            to { opacity: 1; transform: translateY(0); }
        }

        .hero-badge {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            padding: 12px 36px;
            border-radius: 50px;
            background: linear-gradient(135deg, rgba(139,92,246,0.12), rgba(6,182,212,0.12));
            border: 1px solid rgba(139,92,246,0.35);
            color: var(--accent-light);
            font-weight: 700;
            font-size: 0.85rem;
            letter-spacing: 0.2em;
            text-transform: uppercase;
            margin-bottom: 36px;
            position: relative;
            overflow: hidden;
            cursor: default;
            animation: badgeFloat 4s ease-in-out infinite;
        }
        @keyframes badgeFloat {
            0%,100% { transform: translateY(0); }
            50% { transform: translateY(-8px); }
        }
        .hero-badge::before {
            content: '';
            position: absolute;
            top: 0; left: -100%;
            width: 60%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);
            animation: shimmer 3s ease-in-out infinite;
        }
        @keyframes shimmer {
            0% { left: -100%; }
            100% { left: 200%; }
        }
        .hero-badge i { color: var(--primary-light); font-size: 0.9rem; }

        .hero h1 {
            font-size: clamp(3.2rem, 8vw, 6.5rem);
            line-height: 1.05;
            font-weight: 900;
            margin-bottom: 0;
            letter-spacing: -0.02em;
        }
        .hero h1:first-of-type { color: #fff; }
        .hero h1 .gradient-text {
            background: linear-gradient(135deg, var(--primary-light) 0%, var(--accent-light) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: block;
            margin-bottom: 28px;
        }

        .hero p {
            max-width: 680px;
            color: var(--text-muted);
            font-size: 1.2rem;
            margin: 0 auto 52px;
            line-height: 1.9;
            font-weight: 300;
        }

        .hero-actions {
            display: flex;
            gap: 20px;
            justify-content: center;
            flex-wrap: wrap;
        }

        /* ===== BUTTONS ===== */
        .btn {
            padding: 16px 44px;
            border-radius: 14px;
            font-weight: 700;
            font-size: 1rem;
            text-decoration: none;
            transition: all 0.35s var(--ease-bounce);
            display: inline-flex;
            align-items: center;
            gap: 10px;
            border: none;
            cursor: pointer;
            position: relative;
            overflow: hidden;
            letter-spacing: 0.02em;
        }
        .btn::after {
            content: '';
            position: absolute;
            inset: 0;
            background: linear-gradient(135deg, rgba(255,255,255,0.15), transparent);
            opacity: 0;
            transition: opacity 0.3s;
        }
        .btn:hover::after { opacity: 1; }

        .btn-primary {
            background: linear-gradient(135deg, var(--primary), var(--primary-dark));
            color: #fff;
            box-shadow: 0 8px 24px -4px var(--primary-glow);
        }
        .btn-primary:hover {
            transform: translateY(-4px) scale(1.03);
            box-shadow: 0 16px 36px -4px var(--primary-glow);
        }

        .btn-secondary {
            background: transparent;
            border: 1px solid var(--accent);
            color: var(--accent-light);
        }
        .btn-secondary:hover {
            background: var(--accent);
            color: var(--bg-core);
            transform: translateY(-4px) scale(1.03);
            box-shadow: 0 16px 36px -4px var(--accent-glow);
        }

        /* ===== SECTIONS ===== */
        .section-wrapper {
            padding: 130px 5%;
            position: relative;
            overflow: hidden;
            border-top: 1px solid rgba(139,92,246,0.08);
            z-index: 1;
        }
        .bg-alt { background: var(--bg-secondary); }

        .feature-container {
            max-width: 1300px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: 1fr 1.1fr;
            align-items: center;
            gap: 80px;
            position: relative;
            z-index: 2;
        }
        .feature-container.reverse { direction: rtl; }
        .feature-container.reverse > * { direction: ltr; }

        .text-content { z-index: 2; }

        .section-tag {
            display: inline-flex;
            align-items: center;
            gap: 12px;
            font-size: 0.8rem;
            font-weight: 800;
            letter-spacing: 0.25em;
            text-transform: uppercase;
            color: var(--accent-light);
            margin-bottom: 20px;
        }
        .section-tag::before {
            content: '';
            width: 32px;
            height: 2px;
            background: linear-gradient(90deg, var(--primary), var(--accent));
            border-radius: 2px;
            flex-shrink: 0;
        }

        .text-content h2 {
            font-size: clamp(2.4rem, 4vw, 3.8rem);
            margin-bottom: 20px;
            line-height: 1.1;
            font-weight: 900;
            letter-spacing: -0.02em;
            color: #fff;
        }
        .text-content h2 em {
            font-style: normal;
            background: linear-gradient(135deg, var(--primary-light), var(--accent-light));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .text-content p {
            font-size: 1.1rem;
            color: var(--text-muted);
            margin-bottom: 36px;
            line-height: 1.95;
        }

        .specs-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 16px;
        }
        .spec-item {
            display: flex;
            align-items: center;
            gap: 14px;
            padding: 16px 18px;
            border-radius: 14px;
            background: rgba(255,255,255,0.02);
            border: 1px solid rgba(139,92,246,0.1);
            font-weight: 600;
            font-size: 0.9rem;
            color: var(--text-muted);
            transition: all 0.3s var(--ease-out);
            cursor: default;
        }
        .spec-item:hover {
            transform: translateY(-6px);
            border-color: var(--primary);
            background: rgba(139,92,246,0.08);
            color: #fff;
            box-shadow: 0 12px 28px -8px rgba(0,0,0,0.5), 0 0 20px rgba(139,92,246,0.15);
        }
        .icon-box {
            width: 44px;
            height: 44px;
            flex-shrink: 0;
            border-radius: 10px;
            background: linear-gradient(135deg, rgba(139,92,246,0.15), rgba(6,182,212,0.15));
            border: 1px solid rgba(139,92,246,0.2);
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--primary-light);
            font-size: 1.1rem;
            transition: all 0.35s var(--ease-bounce);
        }
        .spec-item:hover .icon-box {
            background: linear-gradient(135deg, var(--primary), var(--accent));
            color: #fff;
            border-color: transparent;
            transform: rotate(10deg) scale(1.1);
            box-shadow: 0 4px 16px var(--primary-glow);
        }

        /* ===== VISUAL CANVAS CONTAINER ===== */
        .visual-content {
            height: 480px;
            border-radius: 24px;
            background: rgba(255,255,255,0.015);
            border: 1px solid rgba(139,92,246,0.12);
            overflow: hidden;
            position: relative;
        }
        .visual-content canvas {
            width: 100% !important;
            height: 100% !important;
            display: block;
        }

        /* ===== CTA SECTION ===== */
        .cta-section {
            padding: 130px 5%;
            text-align: center;
            position: relative;
            z-index: 1;
        }
        .cta-section::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%,-50%);
            width: 600px;
            height: 400px;
            background: radial-gradient(ellipse, rgba(139,92,246,0.12) 0%, transparent 70%);
            pointer-events: none;
        }
        .cta-inner {
            max-width: 760px;
            margin: 0 auto;
            position: relative;
            z-index: 2;
        }
        .cta-inner h2 {
            font-size: clamp(2.8rem, 5vw, 4.5rem);
            font-weight: 900;
            letter-spacing: -0.02em;
            margin-bottom: 20px;
            line-height: 1.1;
        }
        .cta-inner p {
            font-size: 1.15rem;
            color: var(--text-muted);
            margin-bottom: 44px;
            line-height: 1.8;
        }

        /* ===== FOOTER ===== */
        footer {
            background: linear-gradient(180deg, var(--bg-core) 0%, #020408 100%);
            padding: 90px 5% 40px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        footer::before {
            content: '';
            position: absolute;
            top: 0; left: 0;
            width: 100%; height: 1px;
            background: linear-gradient(90deg, transparent, var(--primary), var(--accent), transparent);
        }
        .footer-logo {
            font-size: 3.5rem;
            font-weight: 900;
            background: linear-gradient(135deg, #fff 30%, var(--text-muted));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: inline-block;
            margin-bottom: 12px;
            letter-spacing: -0.02em;
            transition: all 0.4s;
            cursor: default;
        }
        .footer-logo:hover {
            background: linear-gradient(135deg, var(--primary-light), var(--accent-light));
            -webkit-background-clip: text;
        }
        .footer-tag {
            font-size: 1.05rem;
            color: var(--text-light);
            margin-bottom: 44px;
        }
        .contact-info {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-bottom: 36px;
            flex-wrap: wrap;
        }
        .contact-item {
            display: flex;
            align-items: center;
            gap: 10px;
            color: var(--text-muted);
            font-size: 0.95rem;
            padding: 10px 22px;
            border-radius: 50px;
            background: rgba(255,255,255,0.02);
            border: 1px solid rgba(139,92,246,0.1);
            transition: all 0.3s;
        }
        .contact-item:hover {
            border-color: var(--primary);
            color: #fff;
            transform: translateY(-3px);
        }
        .contact-item i { color: var(--accent); }
        .social-grid {
            display: flex;
            justify-content: center;
            gap: 16px;
            margin-bottom: 44px;
        }
        .social-link {
            width: 52px; height: 52px;
            border-radius: 50%;
            background: rgba(255,255,255,0.02);
            border: 1px solid rgba(139,92,246,0.15);
            color: var(--text-muted);
            display: flex; align-items: center; justify-content: center;
            text-decoration: none;
            font-size: 1.25rem;
            transition: all 0.35s var(--ease-bounce);
            position: relative;
            overflow: hidden;
        }
        .social-link::before {
            content: '';
            position: absolute;
            inset: 0;
            background: linear-gradient(135deg, var(--primary), var(--accent));
            opacity: 0;
            transition: opacity 0.3s;
        }
        .social-link i { position: relative; z-index: 1; }
        .social-link:hover::before { opacity: 1; }
        .social-link:hover {
            color: #fff;
            transform: translateY(-5px) scale(1.1);
            border-color: transparent;
            box-shadow: 0 10px 24px var(--primary-glow);
        }
        .copyright {
            color: var(--text-light);
            font-size: 0.9rem;
            padding-top: 36px;
            border-top: 1px solid rgba(139,92,246,0.08);
        }
        .copyright span { font-size: 0.78rem; opacity: 0.6; display: block; margin-top: 6px; }

        /* ===== RESPONSIVE ===== */
        @media (max-width: 1024px) {
            .feature-container,
            .feature-container.reverse {
                grid-template-columns: 1fr;
                direction: ltr;
                text-align: center;
                gap: 50px;
            }
            .section-tag { justify-content: center; }
            .specs-grid { max-width: 480px; margin: 0 auto; }
            .nav-links {
                position: fixed;
                top: 80px;
                left: 50%;
                transform: translateX(-50%) translateY(-120%);
                width: 88%;
                background: rgba(7,9,15,0.97);
                backdrop-filter: blur(24px);
                border: 1px solid var(--border-light);
                border-radius: 20px;
                flex-direction: column;
                padding: 28px;
                opacity: 0;
                visibility: hidden;
                transition: all 0.4s var(--ease-out);
                z-index: 999;
            }
            .nav-links.active {
                transform: translateX(-50%) translateY(0);
                opacity: 1;
                visibility: visible;
            }
            .mobile-toggle { display: flex; }
        }
        @media (max-width: 768px) {
            .navbar { width: 100%; top: 0; border-radius: 0; border-left: none; border-right: none; }
            .navbar.scrolled { top: 0; }
            .hero { padding-top: 110px; }
            .section-wrapper { padding: 80px 5%; }
            .visual-content { height: 320px; }
            .hero-actions { flex-direction: column; align-items: stretch; max-width: 300px; margin: 0 auto; }
            .btn { justify-content: center; }
        }

        /* RTL */
        html[dir="rtl"] .section-tag::before { order: 1; }
        html[dir="rtl"] .brand { flex-direction: row-reverse; }
        html[dir="rtl"] .spec-item { flex-direction: row-reverse; }
        html[dir="rtl"] .hero-badge { flex-direction: row-reverse; }
        html[dir="rtl"] .feature-container { direction: ltr; }
        html[dir="rtl"] .feature-container.reverse { direction: rtl; }
        html[dir="rtl"] .feature-container.reverse > * { direction: rtl; }
        html[dir="rtl"] .section-tag { flex-direction: row-reverse; }
    </style>
</head>
<body>

<!-- PRELOADER -->
<div class="preloader" id="preloader">
    <div class="loader-cube-scene">
        <div class="loader-cube">
            <div class="loader-face front"></div>
            <div class="loader-face back"></div>
            <div class="loader-face left"></div>
            <div class="loader-face right"></div>
            <div class="loader-face top"></div>
            <div class="loader-face bottom"></div>
        </div>
    </div>
    <div class="loader-brand">PlanX</div>
    <div class="progress-container">
        <div class="progress-bar"></div>
    </div>
</div>

<!-- NAV -->
<nav class="navbar" id="navbar">
    <a href="#" class="brand">
        <i class="fa-solid fa-cube"></i>
        PlanX
    </a>

    <button class="mobile-toggle" id="mobileToggle" aria-label="Toggle menu">
        <i class="fa-solid fa-bars"></i>
    </button>

    <div class="nav-links" id="navLinks">
        <a href="#algorithm" class="nav-item" data-en="Algorithm" data-ar="الخوارزمية">Algorithm</a>
        <a href="#experience" class="nav-item" data-en="Experience" data-ar="التجربة">Experience</a>
        <a href="#analytics" class="nav-item" data-en="Analytics" data-ar="التحليل">Analytics</a>
        <a href="#database" class="nav-item" data-en="Database" data-ar="قاعدة البيانات">Database</a>
        <a href="#start" class="nav-item" data-en="Get Started" data-ar="ابدأ الآن">Get Started</a>
    </div>

    <button class="lang-toggle" id="langBtn" aria-label="Toggle language">
        <i class="fa-solid fa-language"></i>
        <span id="langLabel">AR</span>
    </button>
</nav>

<!-- HERO -->
<section class="hero">
    <canvas id="hero-3d-canvas"></canvas>
    <div class="hero-content" id="heroContent">
        <div class="hero-badge">
            <i class="fa-solid fa-bolt"></i>
            <span data-en="Next-Gen Academic Scheduler" data-ar="الجيل الجديد من الجدولة الأكاديمية">Next-Gen Academic Scheduler</span>
        </div>
        <h1 data-en="Complex Schedules." data-ar="الجداول المعقدة.">Complex Schedules.</h1>
        <h1><span class="gradient-text" data-en="Solved Instantly." data-ar="محلولة فوراً.">Solved Instantly.</span></h1>
        <p data-en="PlanX uses advanced AI heuristics to generate conflict-free exam timetables in seconds. Zero overlap, maximum efficiency for every student."
           data-ar="يستخدم PlanX خوارزميات ذكاء اصطناعي متقدمة لإنشاء جداول امتحانات خالية من التعارض في ثوانٍ. صفر تداخل، وكفاءة قصوى لكل طالب.">
           PlanX uses advanced AI heuristics to generate conflict-free exam timetables in seconds. Zero overlap, maximum efficiency for every student.
        </p>
        <div class="hero-actions">
            <a href="workspace.php" class="btn btn-primary">
                <i class="fa-solid fa-rocket"></i>
                <span data-en="Start Scheduling" data-ar="ابدأ الجدولة">Start Scheduling</span>
            </a>
            <a href="#algorithm" class="btn btn-secondary">
                <i class="fa-solid fa-microchip"></i>
                <span data-en="How it Works" data-ar="كيف يعمل">How it Works</span>
            </a>
        </div>
    </div>
</section>

<!-- ALGORITHM -->
<section id="algorithm" class="section-wrapper">
    <div class="feature-container">
        <div class="text-content">
            <span class="section-tag" data-en="Core Algorithm" data-ar="الخوارزمية الأساسية">Core Algorithm</span>
            <h2 data-en="Zero Conflicts. <em>Guaranteed.</em>" data-ar="بدون تعارضات. <em>مضمونة.</em>">Zero Conflicts. <em>Guaranteed.</em></h2>
            <p data-en="Our hybrid heuristic engine analyzes thousands of student enrollments to ensure no student has two exams at the same time — ever."
               data-ar="يقوم محركنا الهجين بتحليل آلاف تسجيلات الطلاب لضمان عدم وجود امتحانين لنفس الطالب في نفس الوقت — أبداً.">
               Our hybrid heuristic engine analyzes thousands of student enrollments to ensure no student has two exams at the same time — ever.
            </p>
            <div class="specs-grid">
                <div class="spec-item"><div class="icon-box"><i class="fa-solid fa-project-diagram"></i></div><span data-en="Graph Coloring" data-ar="تلوين المخطط">Graph Coloring</span></div>
                <div class="spec-item"><div class="icon-box"><i class="fa-solid fa-shield-halved"></i></div><span data-en="Hard Constraints" data-ar="القيود الصارمة">Hard Constraints</span></div>
                <div class="spec-item"><div class="icon-box"><i class="fa-solid fa-users-viewfinder"></i></div><span data-en="Student Grouping" data-ar="تجميع الطلاب">Student Grouping</span></div>
                <div class="spec-item"><div class="icon-box"><i class="fa-solid fa-bug"></i></div><span data-en="Error Detection" data-ar="اكتشاف الأخطاء">Error Detection</span></div>
            </div>
        </div>
        <div class="visual-content" id="algorithm-visual"></div>
    </div>
</section>

<!-- EXPERIENCE -->
<section id="experience" class="section-wrapper bg-alt">
    <div class="feature-container reverse">
        <div class="text-content">
            <span class="section-tag" data-en="Student Experience" data-ar="تجربة الطالب">Student Experience</span>
            <h2 data-en="Minimizing <em>Stress</em>" data-ar="تقليل <em>الضغط</em>">Minimizing <em>Stress</em></h2>
            <p data-en="We don't just fit exams in; we space them out. Our AI reduces consecutive exams to lower the fatigue penalty and keep students performing at their best."
               data-ar="نحن لا نضع الامتحانات فحسب، بل نوزعها بعناية. يقلل ذكاؤنا الاصطناعي من الامتحانات المتتالية للحفاظ على أداء الطلاب في أفضل حالاته.">
               We don't just fit exams in; we space them out. Our AI reduces consecutive exams to lower the fatigue penalty and keep students performing at their best.
            </p>
            <div class="specs-grid">
                <div class="spec-item"><div class="icon-box"><i class="fa-solid fa-stopwatch"></i></div><span data-en="Gap Analysis" data-ar="تحليل الفجوات">Gap Analysis</span></div>
                <div class="spec-item"><div class="icon-box"><i class="fa-solid fa-scale-balanced"></i></div><span data-en="Fair Distribution" data-ar="توزيع عادل">Fair Distribution</span></div>
                <div class="spec-item"><div class="icon-box"><i class="fa-solid fa-thumbs-up"></i></div><span data-en="Low Penalty Score" data-ar="أقل نقاط عقوبة">Low Penalty Score</span></div>
                <div class="spec-item"><div class="icon-box"><i class="fa-solid fa-wand-magic-sparkles"></i></div><span data-en="Auto Optimize" data-ar="تحسين تلقائي">Auto Optimize</span></div>
            </div>
        </div>
        <div class="visual-content" id="experience-visual"></div>
    </div>
</section>

<!-- ANALYTICS -->
<section id="analytics" class="section-wrapper">
    <div class="feature-container">
        <div class="text-content">
            <span class="section-tag" data-en="Data Insights" data-ar="تحليل البيانات">Data Insights</span>
            <h2 data-en="<em>Real-Time</em> Reports" data-ar="تقارير <em>لحظية</em>"><em>Real-Time</em> Reports</h2>
            <p data-en="Visualize room usage, invigilator assignments, and student distribution through interactive dashboards and exportable charts."
               data-ar="شاهد استخدام القاعات، تعيينات المراقبين، وتوزيع الطلاب من خلال لوحات تحكم تفاعلية ورسوم بيانية قابلة للتصدير.">
               Visualize room usage, invigilator assignments, and student distribution through interactive dashboards and exportable charts.
            </p>
            <div class="specs-grid">
                <div class="spec-item"><div class="icon-box"><i class="fa-solid fa-chart-pie"></i></div><span data-en="Capacity Checks" data-ar="فحص السعة">Capacity Checks</span></div>
                <div class="spec-item"><div class="icon-box"><i class="fa-solid fa-clock-rotate-left"></i></div><span data-en="Slot Analysis" data-ar="تحليل الفترات">Slot Analysis</span></div>
                <div class="spec-item"><div class="icon-box"><i class="fa-solid fa-file-csv"></i></div><span data-en="Export CSV" data-ar="تصدير CSV">Export CSV</span></div>
                <div class="spec-item"><div class="icon-box"><i class="fa-solid fa-gauge-high"></i></div><span data-en="Dashboard" data-ar="لوحة التحكم">Dashboard</span></div>
            </div>
        </div>
        <div class="visual-content" id="analytics-visual"></div>
    </div>
</section>

<!-- DATABASE -->
<section id="database" class="section-wrapper bg-alt">
    <div class="feature-container reverse">
        <div class="text-content">
            <span class="section-tag" data-en="Infrastructure" data-ar="البنية التحتية">Infrastructure</span>
            <h2 data-en="<em>Robust</em> Data Handling" data-ar="إدارة بيانات <em>قوية</em>"><em>Robust</em> Data Handling</h2>
            <p data-en="Built on MySQL & PHP. Upload CSVs, manage constraints, and archive past schedules securely and efficiently at any scale."
               data-ar="مبني على MySQL و PHP. ارفع ملفات CSV، أدر القيود، وقم بأرشفة الجداول السابقة بأمان وكفاءة على أي نطاق.">
               Built on MySQL & PHP. Upload CSVs, manage constraints, and archive past schedules securely and efficiently at any scale.
            </p>
            <div class="specs-grid">
                <div class="spec-item"><div class="icon-box"><i class="fa-solid fa-upload"></i></div><span data-en="Mass Import" data-ar="استيراد جماعي">Mass Import</span></div>
                <div class="spec-item"><div class="icon-box"><i class="fa-solid fa-server"></i></div><span data-en="Secure Storage" data-ar="تخزين آمن">Secure Storage</span></div>
                <div class="spec-item"><div class="icon-box"><i class="fa-solid fa-bolt"></i></div><span data-en="Fast Retrieval" data-ar="استرجاع سريع">Fast Retrieval</span></div>
                <div class="spec-item"><div class="icon-box"><i class="fa-solid fa-check-double"></i></div><span data-en="Validation" data-ar="تحقق صحة">Validation</span></div>
            </div>
        </div>
        <div class="visual-content" id="database-visual"></div>
    </div>
</section>

<!-- CTA -->
<section id="start" class="cta-section">
    <div class="cta-inner">
        <span class="section-tag" style="justify-content:center; margin-bottom:24px;" data-en="Ready?" data-ar="جاهز؟">Ready?</span>
        <h2 data-en="Transform Your Academic Calendar" data-ar="حوّل تقويمك الأكاديمي">Transform Your<br><em style="font-style:normal; background:linear-gradient(135deg,var(--primary-light),var(--accent-light)); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">Academic Calendar</em></h2>
        <p data-en="Stop wasting weeks on manual scheduling. Let PlanX do the heavy lifting for you — today."
           data-ar="توقف عن إضاعة الأسابيع في الجدولة اليدوية. دع PlanX يقوم بالمهمة الصعبة بدلاً منك — اليوم.">
           Stop wasting weeks on manual scheduling. Let PlanX do the heavy lifting for you — today.
        </p>
        <a href="workspace.php" class="btn btn-primary" style="font-size:1.15rem; padding:20px 56px;">
            <i class="fa-solid fa-arrow-right"></i>
            <span data-en="Enter Workspace" data-ar="دخول المعمل">Enter Workspace</span>
        </a>
    </div>
</section>

<!-- FOOTER -->
<footer>
    <div class="footer-logo">PlanX</div>
    <div class="footer-tag" data-en="Innovating education through code and strategy." data-ar="نبتكر التعليم من خلال الكود والاستراتيجية.">
        Innovating education through code and strategy.
    </div>
    <div class="contact-info">
        <div class="contact-item"><i class="fa-solid fa-envelope"></i><span>admin@planx.edu</span></div>
        <div class="contact-item"><i class="fa-solid fa-location-dot"></i><span data-en="Faculty of Computers & AI" data-ar="كلية الحاسبات والذكاء الاصطناعي">Faculty of Computers & AI</span></div>
    </div>
    <div class="social-grid">
        <a href="#" class="social-link" aria-label="GitHub"><i class="fa-brands fa-github"></i></a>
        <a href="#" class="social-link" aria-label="LinkedIn"><i class="fa-brands fa-linkedin-in"></i></a>
        <a href="#" class="social-link" aria-label="X/Twitter"><i class="fa-brands fa-x-twitter"></i></a>
        <a href="#" class="social-link" aria-label="Behance"><i class="fa-brands fa-behance"></i></a>
    </div>
    <div class="copyright">
        &copy; 2026 PlanX Scheduling System. All Rights Reserved.
        <span>Graduation Project Team</span>
    </div>
</footer>

<script>
// ========================================
// REGISTER GSAP PLUGINS — MUST BE FIRST
// ========================================
gsap.registerPlugin(ScrollTrigger, ScrollToPlugin);

// ========================================
// PRELOADER
// ========================================
function hidePreloader() {
    const preloader = document.getElementById('preloader');
    preloader.classList.add('hidden');
    // Show hero content
    const heroContent = document.getElementById('heroContent');
    heroContent.classList.add('visible');
    // Init all 3D scenes
    initHero3D();
    initAlgorithmScene();
    initExperienceScene();
    initAnalyticsScene();
    initDatabaseScene();
    initScrollAnimations();
    initActiveNavOnScroll();
}

// Wait at least 2s for the animation, then wait for load
let pageLoaded = false;
let timerDone = false;

window.addEventListener('load', () => {
    pageLoaded = true;
    if (timerDone) hidePreloader();
});

setTimeout(() => {
    timerDone = true;
    if (pageLoaded) hidePreloader();
}, 2200);

// ========================================
// LANGUAGE TOGGLE
// ========================================
let currentLang = 'en';

document.getElementById('langBtn').addEventListener('click', () => {
    currentLang = currentLang === 'en' ? 'ar' : 'en';
    const html = document.documentElement;
    html.lang = currentLang;
    html.dir = currentLang === 'ar' ? 'rtl' : 'ltr';
    document.body.style.fontFamily = currentLang === 'ar' ? 'var(--font-ar)' : 'var(--font-en)';
    document.getElementById('langLabel').textContent = currentLang === 'ar' ? 'EN' : 'AR';

    document.querySelectorAll('[data-en]').forEach(el => {
        const txt = el.getAttribute(`data-${currentLang}`);
        if (!txt) return;
        // Preserve inner HTML for elements with <em>
        if (txt.includes('<em>')) {
            el.innerHTML = txt;
        } else {
            el.textContent = txt;
        }
    });
});

// ========================================
// NAVBAR SCROLL
// ========================================
window.addEventListener('scroll', () => {
    document.getElementById('navbar').classList.toggle('scrolled', window.scrollY > 60);
});

// ========================================
// ACTIVE NAV ON SCROLL
// ========================================
function initActiveNavOnScroll() {
    const sections = document.querySelectorAll('section[id]');
    const navItems = document.querySelectorAll('.nav-item');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const id = entry.target.getAttribute('id');
                navItems.forEach(item => {
                    item.classList.toggle('active', item.getAttribute('href') === `#${id}`);
                });
            }
        });
    }, { rootMargin: '-40% 0px -55% 0px' });

    sections.forEach(s => observer.observe(s));
}

// ========================================
// SMOOTH SCROLL
// ========================================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        const href = this.getAttribute('href');
        if (href === '#') return;
        e.preventDefault();
        const target = document.querySelector(href);
        if (!target) return;
        // Close mobile menu
        document.getElementById('navLinks').classList.remove('active');
        document.getElementById('mobileToggle').innerHTML = '<i class="fa-solid fa-bars"></i>';

        gsap.to(window, {
            duration: 1.1,
            scrollTo: { y: target, offsetY: 90 },
            ease: 'power3.inOut'
        });
    });
});

// ========================================
// MOBILE MENU
// ========================================
const mobileToggle = document.getElementById('mobileToggle');
const navLinks = document.getElementById('navLinks');

mobileToggle.addEventListener('click', () => {
    const isOpen = navLinks.classList.toggle('active');
    mobileToggle.innerHTML = isOpen
        ? '<i class="fa-solid fa-times"></i>'
        : '<i class="fa-solid fa-bars"></i>';
});

document.addEventListener('click', (e) => {
    if (!navLinks.contains(e.target) && !mobileToggle.contains(e.target)) {
        navLinks.classList.remove('active');
        mobileToggle.innerHTML = '<i class="fa-solid fa-bars"></i>';
    }
});

// ========================================
// HELPER: Make a renderer fitted to a container
// ========================================
function makeRenderer(container) {
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setClearColor(0x000000, 0);
    container.appendChild(renderer.domElement);
    return renderer;
}

// ========================================
// HERO 3D SCENE
// ========================================
function initHero3D() {
    const canvas = document.getElementById('hero-3d-canvas');
    if (!canvas) return;

    const scene = new THREE.Scene();
    const W = window.innerWidth, H = window.innerHeight;
    const camera = new THREE.PerspectiveCamera(70, W / H, 0.1, 500);
    camera.position.z = 14;

    const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setSize(W, H);
    renderer.setClearColor(0x000000, 0);

    // Lights
    scene.add(new THREE.AmbientLight(0x404060, 0.8));
    const pL1 = new THREE.PointLight(0x8b5cf6, 3, 40);
    pL1.position.set(6, 6, 6);
    scene.add(pL1);
    const pL2 = new THREE.PointLight(0x06b6d4, 3, 40);
    pL2.position.set(-6, -3, 8);
    scene.add(pL2);

    const geos = [
        new THREE.BoxGeometry(1.2, 1.2, 1.2),
        new THREE.IcosahedronGeometry(0.8, 0),
        new THREE.TorusGeometry(0.6, 0.22, 12, 28),
        new THREE.OctahedronGeometry(0.9),
        new THREE.TetrahedronGeometry(0.9)
    ];
    const colors = [0x8b5cf6, 0x06b6d4, 0xa78bfa, 0x22d3ee, 0xddd6fe];

    const shapes = [];
    const count = 20;
    for (let i = 0; i < count; i++) {
        const geo = geos[i % geos.length];
        const isWire = i % 4 === 0;
        const mat = new THREE.MeshStandardMaterial({
            color: colors[i % colors.length],
            roughness: 0.25,
            metalness: 0.35,
            transparent: true,
            opacity: isWire ? 0.4 : 0.75,
            wireframe: isWire
        });
        const mesh = new THREE.Mesh(geo, mat);

        // Distribute in a sphere shell
        const r = 7 + Math.random() * 5;
        const theta = Math.random() * Math.PI * 2;
        const phi = Math.acos(2 * Math.random() - 1);
        mesh.position.set(
            r * Math.sin(phi) * Math.cos(theta),
            r * Math.sin(phi) * Math.sin(theta),
            r * Math.cos(phi)
        );
        mesh.userData = {
            rx: (Math.random() - 0.5) * 0.012,
            ry: (Math.random() - 0.5) * 0.012,
            baseY: mesh.position.y,
            floatSpeed: 0.0005 + Math.random() * 0.001,
            floatPhase: Math.random() * Math.PI * 2
        };
        scene.add(mesh);
        shapes.push(mesh);
    }

    let mx = 0, my = 0;
    window.addEventListener('mousemove', e => {
        mx = (e.clientX / window.innerWidth - 0.5) * 3;
        my = -(e.clientY / window.innerHeight - 0.5) * 3;
    });

    function animate() {
        requestAnimationFrame(animate);
        const t = Date.now();
        shapes.forEach(s => {
            s.rotation.x += s.userData.rx;
            s.rotation.y += s.userData.ry;
            s.position.y = s.userData.baseY + Math.sin(t * s.userData.floatSpeed + s.userData.floatPhase) * 0.6;
        });
        camera.position.x += (mx - camera.position.x) * 0.03;
        camera.position.y += (my - camera.position.y) * 0.03;
        camera.lookAt(scene.position);
        renderer.render(scene, camera);
    }
    animate();

    window.addEventListener('resize', () => {
        const W = window.innerWidth, H = window.innerHeight;
        camera.aspect = W / H;
        camera.updateProjectionMatrix();
        renderer.setSize(W, H);
    });
}

// ========================================
// ALGORITHM SCENE — Graph / Network
// ========================================
function initAlgorithmScene() {
    const container = document.getElementById('algorithm-visual');
    if (!container) return;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 100);
    camera.position.set(0, 1.5, 8);

    const renderer = makeRenderer(container);

    scene.add(new THREE.AmbientLight(0xaaaacc, 0.6));
    const pL = new THREE.PointLight(0x8b5cf6, 4, 20);
    pL.position.set(3, 3, 3);
    scene.add(pL);
    const pL2 = new THREE.PointLight(0x06b6d4, 3, 20);
    pL2.position.set(-3, -2, 3);
    scene.add(pL2);

    // Node positions
    const nodePositions = [
        new THREE.Vector3(0, 0, 0),
        new THREE.Vector3(2.5, 1.5, -0.5),
        new THREE.Vector3(-2.5, 1.2, 0.3),
        new THREE.Vector3(1.8, -1.8, 0.5),
        new THREE.Vector3(-1.8, -1.5, -0.5),
        new THREE.Vector3(0, 2.8, 0.2),
    ];
    const nodeColors = [0x8b5cf6, 0x06b6d4, 0xa78bfa, 0x22d3ee, 0x6d28d9, 0x0891b2];

    const group = new THREE.Group();
    const nodes = [];

    nodePositions.forEach((pos, i) => {
        const geo = new THREE.SphereGeometry(0.35, 24, 24);
        const mat = new THREE.MeshStandardMaterial({
            color: nodeColors[i],
            roughness: 0.2,
            metalness: 0.5,
            emissive: nodeColors[i],
            emissiveIntensity: 0.2
        });
        const node = new THREE.Mesh(geo, mat);
        node.position.copy(pos);
        group.add(node);
        nodes.push(node);

        // Ring around each node
        const rGeo = new THREE.TorusGeometry(0.5, 0.03, 8, 24);
        const rMat = new THREE.MeshStandardMaterial({ color: nodeColors[i], transparent: true, opacity: 0.4 });
        const ring = new THREE.Mesh(rGeo, rMat);
        ring.position.copy(pos);
        ring.rotation.x = Math.PI / 2;
        group.add(ring);
    });

    // Edges
    const edges = [[0,1],[0,2],[0,3],[0,4],[1,5],[2,5],[3,4],[1,3],[2,4]];
    edges.forEach(([a, b]) => {
        const pts = [nodePositions[a], nodePositions[b]];
        const geo = new THREE.BufferGeometry().setFromPoints(pts);
        const mat = new THREE.LineBasicMaterial({ color: 0x8b5cf6, transparent: true, opacity: 0.35 });
        group.add(new THREE.Line(geo, mat));
    });

    scene.add(group);

    let raf;
    function animate() {
        raf = requestAnimationFrame(animate);
        group.rotation.y += 0.004;
        group.rotation.x = Math.sin(Date.now() * 0.0007) * 0.12;
        // Pulse nodes
        nodes.forEach((n, i) => {
            const s = 1 + Math.sin(Date.now() * 0.002 + i) * 0.07;
            n.scale.setScalar(s);
        });
        renderer.render(scene, camera);
    }
    animate();

    const obs = new ResizeObserver(() => {
        camera.aspect = container.clientWidth / container.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(container.clientWidth, container.clientHeight);
    });
    obs.observe(container);
}

// ========================================
// EXPERIENCE SCENE — Calendar / Timeline
// ========================================
function initExperienceScene() {
    const container = document.getElementById('experience-visual');
    if (!container) return;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 100);
    camera.position.set(0, 0, 8);

    const renderer = makeRenderer(container);

    scene.add(new THREE.AmbientLight(0xaaccff, 0.5));
    const pL = new THREE.PointLight(0x06b6d4, 4, 20);
    pL.position.set(3, 3, 4);
    scene.add(pL);
    const pL2 = new THREE.PointLight(0x8b5cf6, 3, 20);
    pL2.position.set(-3, -2, 4);
    scene.add(pL2);

    const group = new THREE.Group();

    // Calendar grid (5 x 4)
    const cols = 5, rows = 4;
    const spacing = 1.0;
    const eventColors = [0x8b5cf6, 0x06b6d4, 0xa78bfa, 0x22d3ee];

    for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
            const isEvent = Math.random() > 0.55;
            const h = isEvent ? 0.55 + Math.random() * 0.4 : 0.15;
            const geo = new THREE.BoxGeometry(0.7, h, 0.7);
            const color = isEvent ? eventColors[Math.floor(Math.random() * eventColors.length)] : 0x1e2a3a;
            const mat = new THREE.MeshStandardMaterial({
                color,
                roughness: 0.3,
                metalness: 0.2,
                transparent: true,
                opacity: isEvent ? 0.9 : 0.5,
                emissive: isEvent ? color : 0x000000,
                emissiveIntensity: isEvent ? 0.15 : 0
            });
            const box = new THREE.Mesh(geo, mat);
            box.position.set(
                (c - (cols-1)/2) * spacing,
                h / 2 - 1.5,
                (r - (rows-1)/2) * spacing
            );
            box.userData = { isEvent, baseH: h, phase: Math.random() * Math.PI * 2 };
            group.add(box);
        }
    }

    // Grid platform
    const platformGeo = new THREE.BoxGeometry(cols * spacing + 0.3, 0.08, rows * spacing + 0.3);
    const platformMat = new THREE.MeshStandardMaterial({ color: 0x0d1a2d, roughness: 0.8 });
    const platform = new THREE.Mesh(platformGeo, platformMat);
    platform.position.y = -1.55;
    group.add(platform);

    scene.add(group);

    function animate() {
        requestAnimationFrame(animate);
        group.rotation.y += 0.004;
        group.rotation.x = Math.sin(Date.now() * 0.0006) * 0.08;
        group.children.forEach(child => {
            if (child.userData && child.userData.isEvent) {
                const pulse = 1 + Math.sin(Date.now() * 0.002 + child.userData.phase) * 0.05;
                child.scale.y = pulse;
            }
        });
        renderer.render(scene, camera);
    }
    animate();

    const obs = new ResizeObserver(() => {
        camera.aspect = container.clientWidth / container.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(container.clientWidth, container.clientHeight);
    });
    obs.observe(container);
}

// ========================================
// ANALYTICS SCENE — 3D Bar Chart
// ========================================
function initAnalyticsScene() {
    const container = document.getElementById('analytics-visual');
    if (!container) return;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 100);
    camera.position.set(0, 2.5, 9);
    camera.lookAt(0, 0, 0);

    const renderer = makeRenderer(container);

    scene.add(new THREE.AmbientLight(0xaaaacc, 0.6));
    const pL = new THREE.PointLight(0x8b5cf6, 4, 20);
    pL.position.set(4, 6, 4);
    scene.add(pL);
    const pL2 = new THREE.PointLight(0x06b6d4, 3, 20);
    pL2.position.set(-4, 2, 4);
    scene.add(pL2);

    const group = new THREE.Group();
    const barData = [1.2, 2.4, 1.6, 3.0, 1.8, 2.2, 2.7, 1.4];
    const palette = [0x8b5cf6, 0x06b6d4, 0xa78bfa, 0x22d3ee, 0x7c3aed, 0x0891b2, 0xc4b5fd, 0x67e8f9];

    barData.forEach((h, i) => {
        const geo = new THREE.BoxGeometry(0.55, h, 0.55);
        const mat = new THREE.MeshStandardMaterial({
            color: palette[i],
            roughness: 0.25,
            metalness: 0.2,
            emissive: palette[i],
            emissiveIntensity: 0.12
        });
        const bar = new THREE.Mesh(geo, mat);
        bar.position.set((i - (barData.length-1)/2) * 0.85, h/2 - 1.8, 0);
        bar.userData = { targetH: h, phase: i * 0.4 };
        group.add(bar);

        // Glow cap on top
        const capGeo = new THREE.BoxGeometry(0.6, 0.08, 0.6);
        const capMat = new THREE.MeshStandardMaterial({ color: 0xffffff, emissive: palette[i], emissiveIntensity: 0.6, transparent: true, opacity: 0.8 });
        const cap = new THREE.Mesh(capGeo, capMat);
        cap.position.set(bar.position.x, h - 1.76, 0);
        group.add(cap);
    });

    // Base
    const baseGeo = new THREE.BoxGeometry(barData.length * 0.85 + 0.5, 0.1, 1.5);
    const baseMat = new THREE.MeshStandardMaterial({ color: 0x101825, roughness: 0.8 });
    const base = new THREE.Mesh(baseGeo, baseMat);
    base.position.y = -1.85;
    group.add(base);

    scene.add(group);

    function animate() {
        requestAnimationFrame(animate);
        group.rotation.y += 0.003;
        group.rotation.x = Math.sin(Date.now() * 0.0005) * 0.06;
        renderer.render(scene, camera);
    }
    animate();

    const obs = new ResizeObserver(() => {
        camera.aspect = container.clientWidth / container.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(container.clientWidth, container.clientHeight);
    });
    obs.observe(container);
}

// ========================================
// DATABASE SCENE — Layered Cylinders + Particles
// ========================================
function initDatabaseScene() {
    const container = document.getElementById('database-visual');
    if (!container) return;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 100);
    camera.position.set(0, 1.5, 8);

    const renderer = makeRenderer(container);

    scene.add(new THREE.AmbientLight(0xaaccff, 0.5));
    const pL = new THREE.PointLight(0x8b5cf6, 4, 20);
    pL.position.set(3, 4, 4);
    scene.add(pL);
    const pL2 = new THREE.PointLight(0x06b6d4, 3, 20);
    pL2.position.set(-3, -1, 4);
    scene.add(pL2);

    const group = new THREE.Group();
    const layerColors = [0x8b5cf6, 0x06b6d4, 0xa78bfa, 0x22d3ee];
    const numLayers = 4;

    for (let i = 0; i < numLayers; i++) {
        const bodyGeo = new THREE.CylinderGeometry(1.2, 1.2, 0.5, 40);
        const bodyMat = new THREE.MeshStandardMaterial({
            color: layerColors[i],
            roughness: 0.3,
            metalness: 0.3,
            transparent: true,
            opacity: 0.85,
            emissive: layerColors[i],
            emissiveIntensity: 0.1
        });
        const cyl = new THREE.Mesh(bodyGeo, bodyMat);
        cyl.position.y = i * 0.75 - 1.2;
        group.add(cyl);

        // Top & bottom cap rims
        [-0.275, 0.275].forEach(dy => {
            const rimGeo = new THREE.TorusGeometry(1.2, 0.04, 8, 40);
            const rimMat = new THREE.MeshStandardMaterial({ color: 0xffffff, emissive: layerColors[i], emissiveIntensity: 0.5, transparent: true, opacity: 0.7 });
            const rim = new THREE.Mesh(rimGeo, rimMat);
            rim.position.y = cyl.position.y + dy;
            group.add(rim);
        });
    }

    // Orbiting data particles
    const particles = [];
    for (let i = 0; i < 40; i++) {
        const pGeo = new THREE.SphereGeometry(0.06, 6, 6);
        const pMat = new THREE.MeshStandardMaterial({
            color: i % 2 === 0 ? 0x06b6d4 : 0xa78bfa,
            emissive: i % 2 === 0 ? 0x06b6d4 : 0xa78bfa,
            emissiveIntensity: 0.6
        });
        const p = new THREE.Mesh(pGeo, pMat);
        p.userData = {
            angle: (i / 40) * Math.PI * 2,
            radius: 1.7 + Math.random() * 0.6,
            yBase: -1.5 + Math.random() * 3,
            speed: 0.006 + Math.random() * 0.006
        };
        scene.add(p);
        particles.push(p);
    }

    scene.add(group);

    function animate() {
        requestAnimationFrame(animate);
        group.rotation.y += 0.005;
        particles.forEach(p => {
            p.userData.angle += p.userData.speed;
            p.position.x = Math.cos(p.userData.angle) * p.userData.radius;
            p.position.z = Math.sin(p.userData.angle) * p.userData.radius;
            p.position.y = p.userData.yBase + Math.sin(Date.now() * 0.001 + p.userData.angle) * 0.3;
        });
        renderer.render(scene, camera);
    }
    animate();

    const obs = new ResizeObserver(() => {
        camera.aspect = container.clientWidth / container.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(container.clientWidth, container.clientHeight);
    });
    obs.observe(container);
}

// ========================================
// SCROLL ANIMATIONS
// ========================================
function initScrollAnimations() {
    // Text content slide in
    gsap.utils.toArray('.text-content').forEach((el, i) => {
        const dir = i % 2 === 0 ? -60 : 60;
        gsap.fromTo(el,
            { x: dir, opacity: 0 },
            {
                x: 0, opacity: 1, duration: 0.9,
                ease: 'power3.out',
                scrollTrigger: { trigger: el, start: 'top 82%', toggleActions: 'play none none reverse' }
            }
        );
    });

    // Visual content scale in
    gsap.utils.toArray('.visual-content').forEach(el => {
        gsap.fromTo(el,
            { scale: 0.88, opacity: 0 },
            {
                scale: 1, opacity: 1, duration: 0.9,
                ease: 'power3.out',
                scrollTrigger: { trigger: el, start: 'top 82%', toggleActions: 'play none none reverse' }
            }
        );
    });

    // Spec items stagger
    gsap.utils.toArray('.specs-grid').forEach(grid => {
        gsap.fromTo(grid.children,
            { y: 30, opacity: 0 },
            {
                y: 0, opacity: 1, duration: 0.6,
                ease: 'power2.out',
                stagger: 0.08,
                scrollTrigger: { trigger: grid, start: 'top 85%', toggleActions: 'play none none reverse' }
            }
        );
    });

    // CTA
    gsap.fromTo('.cta-inner',
        { y: 40, opacity: 0 },
        {
            y: 0, opacity: 1, duration: 1,
            ease: 'power3.out',
            scrollTrigger: { trigger: '.cta-section', start: 'top 80%', toggleActions: 'play none none reverse' }
        }
    );
}
</script>
</body>
</html>