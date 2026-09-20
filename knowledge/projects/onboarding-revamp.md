# Onboarding Revamp

## Goal

Reduce time-to-first-value for new users by cutting the onboarding flow from 7
steps to 3, and by deferring optional profile fields to post-signup.

## What changed

The signup form now only collects email, password, and workspace name. Company
size, industry, and integration preferences moved to an optional "complete your
profile" prompt shown after the user's first successful action in the product.

## Results

Signup completion rate improved, but this note doesn't track exact numbers —
see the analytics dashboard for current conversion figures. The main engineering
takeaway: deferring optional fields to post-activation is a repeatable pattern
worth applying to other flows.
