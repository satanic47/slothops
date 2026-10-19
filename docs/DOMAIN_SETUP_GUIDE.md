# 🌐 .tech Domain Setup Guide for SlothOps

This guide explains how to claim your free `.tech` domain via Hacktoberfest 2026 and connect it to your Render deployment.

---

## Step 1: Claim Your Free .tech Domain
1. Log in to [hacktoberfest.com/my/promos](https://hacktoberfest.com/my/promos/).
2. Locate the **.tech Domains** offer banner.
3. Click **Claim Promo Code** to copy your unique voucher code.
4. Go to [get.tech](https://get.tech) and search for your preferred domain:
   - Recommended: `slothops.tech` (or `slothflow.tech`, `lazydev.tech`).
5. Apply your voucher code at checkout to register the domain for **1 year free**.

---

## Step 2: Configure Render Web Service
1. Log in to [dashboard.render.com](https://dashboard.render.com).
2. Open your `slothops-web` service.
3. In the left navigation menu, click **Settings**.
4. Scroll down to **Custom Domains**.
5. Click **Add Custom Domain** and enter:
   - `slothops.tech` (and optionally `www.slothops.tech`).
6. Render will provide you with your target CNAME value:
   - Example: `slothops.onrender.com`.

---

## Step 3: Add DNS Records in your .tech Registrar
1. In your domain registrar's DNS Management console:
2. Add a **CNAME** record:
   - **Type:** `CNAME`
   - **Name / Host:** `www` (or `@` if your registrar supports CNAME flattening / ALIAS / ANAME)
   - **Value / Target:** `slothops.onrender.com`
   - **TTL:** `300` (or Automatic)
3. If using root domain `@` without CNAME flattening, add an `A` record pointing to Render's IP address (provided in your Render dashboard).

---

## Step 4: Verification & Automated TLS/SSL
- Render automatically detects the DNS records once propagated (usually 2–15 minutes).
- Let's Encrypt TLS/SSL certificates are issued and managed automatically by Render with zero maintenance.
- Verify status in SlothOps: Visit [http://localhost:8000/api/domain/verify](http://localhost:8000/api/domain/verify) or open the SlothOps dashboard.
