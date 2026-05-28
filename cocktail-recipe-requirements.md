# Cocktail Recipe Project Requirements
Project: CocktailBook (inspired by RecipeHub layout)
Document version: 1.0
Last updated: 2026-05-05

## 1. Project Overview
Build a digital cocktail recipe application that lets users discover, store, customize, and share cocktail recipes. Support browsing by ingredients, techniques, glassware, taste profile, and occasion.

## 2. Objectives
- Provide a searchable, filterable catalog of cocktail recipes.
- Enable users to save favorites, create collections, and submit recipes.
- Offer accurate ingredient scaling, step-by-step instructions, and visual assets.
- Support offline viewing of saved recipes and cross-device sync.

## 3. Scope
In scope:
- Recipe CRUD for users and admins.
- Ingredient parsing and unit conversion (metric/imperial).
- User accounts, authentication, and profile settings.
- Browsing, search, filters, and recommendations.
- Ratings, comments, and social sharing.
Out of scope (phase 1):
- In-app alcohol purchase or age-verification hardware.
- Live video mixing instructions.

## 4. User Personas
- Home Enthusiast: searches recipes, saves favorites, follows creators.
- Professional Bartender: submits advanced recipes, tags techniques.
- Casual Guest: views recipes and shares via social links.
- Admin: moderates content, manages categories and reports.

## 5. Key Features
- Recipe view: title, author, photo, ingredients (quantities), steps, prep time, difficulty, tags, glassware, garnish, ABV estimate.
- Ingredient scaling: adjust servings and units.
- Search & filters: full-text, ingredient include/exclude, taste profile, difficulty, time.
- Collections & favorites: private/public lists.
- Submit/Edit workflow: draft, validation, moderation queue.
- Offline support: cache saved recipes.
- Social: share link, export printable recipe card.
- Analytics: popular recipes, trends.

## 6. User Stories (examples)
- As a user I can search by ingredient so I can find cocktails I can make now.
- As a user I can scale ingredient quantities so I can make any number of servings.
- As a contributor I can submit a recipe for review so it appears in the catalog after approval.

## 7. Functional Requirements
- FR1: Register/login with email + OAuth (Google, Apple).
- FR2: Create/read/update/delete recipes with version history.
- FR3: Parse ingredient lines into quantity, unit, ingredient, notes.
- FR4: Convert units between metric and imperial.
- FR5: Full-text search and tag-based filtering.
- FR6: Rating (1–5) and comments with moderation tools.
- FR7: Recipe sharing via URL and social platforms.
- FR8: Export recipe as printable PDF.

## 8. Non-Functional Requirements
- NFR1: Response time < 300ms for search queries.
- NFR2: Offline read for saved recipes within 24 hours of save.
- NFR3: Availability 99.9% monthly.
- NFR4: Data backup daily, retention 30 days.
- NFR5: Scalable to 1M users.

## 9. Data Model (high level)
- User { id, name, email, authProviders, preferences, createdAt }
- Recipe { id, title, authorId, ingredients[], steps[], photos[], tags[], servings, prepTime, difficulty, abvEstimate, status, createdAt }
- Ingredient { name, quantity, unit, preparation }
- Collection { id, ownerId, title, recipeIds[], visibility }
- Rating { userId, recipeId, score }
- Comment { userId, recipeId, body, createdAt, moderated }

## 10. API Endpoints (examples)
- GET /recipes?query=&filters=
- GET /recipes/{id}
- POST /recipes
- PUT /recipes/{id}
- POST /auth/login
- POST /users/{id}/collections

## 11. UX & Accessibility
- Mobile-first responsive UI.
- Clear recipe step sequencing and timers.
- WCAG 2.1 AA compliance: keyboard navigation, semantic HTML, alt text for images, color contrast.

## 12. Security & Privacy
- Encrypt sensitive data at rest and in transit (TLS).
- Rate limit public endpoints.
- Age-gating optional (display advisory).
- Comply with GDPR: user data export & delete.

## 13. Testing & Acceptance Criteria
- Unit tests for parsing and scaling logic (>=90% coverage).
- Integration tests for search and submission flow.
- Manual UX testing on major devices and browsers.
- Acceptance: core flows (search, view, save, submit) pass end-to-end tests.

## 14. Metrics & Analytics
- Track DAU/MAU, conversion (signup after view), recipe saves, share rate, average rating.
- A/B test homepage recommendation algorithms.

## 15. Roadmap / Milestones
- M1 (4 weeks): Core data model, recipe CRUD, basic UI.
- M2 (8 weeks): Search, filtering, scaling, unit conversion.
- M3 (12 weeks): Authentication, submissions, moderation.
- M4 (16 weeks): Offline support, PDF export, analytics.

## 16. Open Questions
- Moderation model: community vs. centralized?
- Level of ingredient normalization required for recommendation quality.