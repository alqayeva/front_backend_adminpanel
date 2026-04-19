# Progress

## Umumi veziyyet
- Hazirda `Task 7`, `Task 8` ve `Task 9` `users` modulu uzre backend terefde implement olunub.
- Bu tasklar ucun avtomat testler ugurla kecib.
- `Task 8` ve `Task 9` ucun Postman testleri hele edilmeyib, sabaha saxlanilib.
- `products` modulu hazir olmadigi ucun eyni tasklarin `products` terefleri hele tamamlanmayib.

## Task 7 - Filter / Search / Pagination

### Status
- `users` modulu ucun tamamlanib.
- Butov layihe seviyyesinde tam baglanmayib, cunki `products` modulu hele hazir deyil.

### Tamamlanan isler
- `GET /api/users/` endpoint-i elave olundu.
- Endpoint `IsAuthenticated` ile qorundu.
- `search` desteyi elave olundu:
  - `username`
  - `email`
- `filter` desteyi elave olundu:
  - `is_active`
- `pagination` aktiv edildi:
  - `page`
  - `page_size`
- `ordering` desteyi elave olundu:
  - `created_at`
  - `username`
  - `email`
- Default ordering `-created_at` secildi.
- `UserListSerializer` yaradildi.
- `apps/user/urls.py` ve `core/urls.py` daxilinde route-lar qoshuldu.
- API davranishini yoxlayan testler yazildi.
- Postman ile de yoxlanildi:
  - token olmadan `401`
  - token ile `200`
  - search, filter, pagination ve ordering davranishi yoxlanildi

### Deyisdirilen fayllar
- `apps/user/serializers.py`
- `apps/user/views.py`
- `apps/user/urls.py`
- `core/urls.py`
- `apps/user/tests.py`

### Qalan hisseler
- `products` modulu ucun Task 7 hele edilmeyib.
- Sebeb:
  - `apps/products/models.py` bosdur
  - `products` ucun serializer/view/url qatlari yoxdur
  - search/filter field-lerini duzgun secmek ucun model field-leri lazimdir

## Task 8 - File Upload

### Status
- `users` modulu ucun backend terefde tamamlanib.
- Postman testi hele edilmeyib.
- `products` terefde hele edilmeyib.

### Tamamlanan isler
- `PATCH /api/users/me/avatar/` endpoint-i elave olundu.
- Auth olunmus user-in oz avatarini yenilemesi quruldu.
- `multipart/form-data` qebulu aktiv edildi.
- Avatar upload ucun ayri serializer yazildi.
- Validation elave olundu:
  - icazeli formatlar: `jpg`, `jpeg`, `png`, `webp`
  - olcu limiti: default `2 MB`
- Development ucun `MEDIA_URL` route-u qoshuldu.
- Avatar upload davranishini yoxlayan testler yazildi:
  - auth olmadan upload
  - valid image upload
  - invalid file type
  - oversized image

### Deyisdirilen fayllar
- `apps/user/serializers.py`
- `apps/user/views.py`
- `apps/user/urls.py`
- `core/urls.py`
- `apps/user/tests.py`

### Qalan hisseler
- Postman ile manual avatar upload testi qalir.
- `products` image upload hissesi hele edilmir, cunki `products` modulu hazir deyil.

## Task 9 - Error Handling / Standard Response Format

### Status
- Backend terefde tamamlanib.
- Postman testi hele edilmeyib.

### Tamamlanan isler
- Standard success response formati aktiv edildi:
  - `success`
  - `data`
  - `message`
- Standard error response formati aktiv edildi:
  - `success`
  - `error`
- Pagination response-lari da yeni envelope-a salindi.
- Global exception handler yazildi.
- DRF validation/auth xetalari standart string error formatina cevrildi.
- `GET /api/users/` endpoint-i yeni success formatina kecirildi.
- `PATCH /api/users/me/avatar/` endpoint-i yeni success formatina kecirildi.
- Testler yeni response formatina uygun sekilde yenilendi.

### Deyisdirilen fayllar
- `utils/response.py`
- `utils/exceptions.py`
- `utils/pagination.py`
- `apps/user/views.py`
- `apps/user/tests.py`

### Qalan hisseler
- Postman ile success/error response formatlarinin manual yoxlanmasi qalir.
- Future endpoint-ler geldikce eyni response standardi onlara da tetbiq olunmalidir.

## Task 10 - Performance

### Status
- Bu merhelede `users` modulu ucun minimal ve menali optimizasiya edilib.
- `products` ve relation-li hisseler hele hazir olmadigi ucun Task 10 butov layihe seviyyesinde tamamlanmayib.

### Tamamlanan isler
- `GET /api/users/` queryset-i yungullesdirildi.
- List endpoint ucun yalniz serializerin istifade etdiyi field-ler secildi:
  - `id`
  - `username`
  - `email`
  - `first_name`
  - `last_name`
  - `role`
  - `is_active`
  - `avatar`
  - `created_at`
- Kodda qeyd olundu ki, hazirki `users` endpoint-inde relation olmadigi ucun
  `select_related/prefetch_related` bu merhelede menali deyil.

### Deyisdirilen fayllar
- `apps/user/views.py`

### Qalan hisseler
- `Task 1-6` tamamlandiqdan sonra relation-li endpoint-ler gelerse
  `select_related/prefetch_related` yeniden qiymetlendirilmelidir.
- `products` modulu hazir olduqdan sonra Task 10-un products hissesi ayrica tamamlanmalidir.
- Caching/Redis bu merhelede tetbiq olunmayib.

## Task 11 - API Documentation

### Status
- Bu merhelede movcud backend hissesi ucun tamamlanib.
- Swagger / OpenAPI docs endpoint-i elave olunub.
- Manual yoxlama hele edilmeyib.

### Tamamlanan isler
- `GET /api/docs` endpoint-i elave olundu.
- Swagger UI quruldu.
- API title, version ve description verildi.
- Hazirda movcud olan `users` endpoint-leri ucun esas izahlar docs-a elave olundu.
- Docs endpoint-in acildigini yoxlayan test yazildi.

### Deyisdirilen fayllar
- `core/urls.py`
- `apps/user/views.py`
- `core/tests.py`

### Qalan hisseler
- Brauzerde manual yoxlama qalir.
- `Task 1-6` tamamlandiqdan sonra auth, products ve diger endpoint-ler geldikce docs genisletdirilmelidir.

## Task 12 - Git Workflow

### Status
- Praktik workflow qaydasi hazirlanib.
- `GIT_WORKFLOW.md` faylinda addim-addim qeyd olunub.
- Branch yaratmaq, commit, push ve PR acmaq hissesini sen manuel icra edeceksen.

### Tamamlanan isler
- Hazirki isler ucun teklif olunan branch adi secildi:
  - `feature/users`
- Git workflow ayrica senedlesdirildi.
- PR description ve review mentiqi qeyd olundu.
- Merge conflict olduqda nece hereket etmek lazim oldugu qeyd olundu.
- `token.md` faylinin sehvən commit olunmamasi ucun `.gitignore` yenilendi.

### Deyisdirilen fayllar
- `GIT_WORKFLOW.md`
- `.gitignore`

### Qalan hisseler
- `git switch -c feature/users`
- `git add ...`
- `git commit`
- `git push -u origin feature/users`
- GitHub-da PR acilmasi
- Son review ve merge

## Test neticesi
- Ishledilen komanda:
  - `..\venv\Scripts\python.exe manage.py test apps.user.tests core.tests`
- Son netice:
  - `16` test ugurla kecdi

## Umumi qalan hisseler
- `Task 8` Postman testi qalir.
- `Task 9` Postman testi qalir.
- `Task 11` brauzerde manual yoxlamasi qalir.
- `Task 12` ucun branch yaratmaq, commit etmek, push etmek ve PR acmaq qalir.
- `products` modulu hazir olduqdan sonra `Task 7` ve mumkun olarsa `Task 8` terefleri orada da tamamlanmalidir.
- Diger developer `Task 1-6`-ni bitirenden sonra merge ve inteqrasiya yoxlamasi edilmelidir.

## Novbeti addim
- Sabah `Task 8` ve `Task 9` Postman testleri edilmelidir.
- `Task 11` docs endpoint-i de manual olaraq brauzerde yoxlanmalidir.
- Sonra `feature/users` branch-i yaradilib commit ve PR axini icra edilmelidir.
