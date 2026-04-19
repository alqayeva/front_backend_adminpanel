# Git Workflow

## Task 12 meqsedi
Bu layihede isler birbasha `main` branch-inde edilmemelidir.
Her is ayri feature branch-inde gorulmeli, sonra GitHub-a push olunmali,
Pull Request acilmali ve code review-den sonra merge edilmelidir.

## Hazirki veziyyet
- Hazirda lokal deyisiklikler `main` branch-i uzerindedir.
- Bu deyisiklikler push olunmamishdan evvel feature branch-e kecirilmelidir.
- Hazirki islerin mecmusu en cox `users` modulu ve ortaq util qatlarina aiddir.

## Bu merhelede teklif olunan branch
- `feature/users`

Sebeb:
- Task 7, 8, 9, 10 ve 11-in hazirda edilen hisseleri esasen `users` modulu uzerindedir.
- `products` modulu hele hazir deyil.
- `auth` modulu de hele ayri islenmeyib.

## Praktik addimlar

### 1. Hazirki deyisiklikleri feature branch-e kecir
```bash
git switch -c feature/users
```

Bu komanda hazir `main` uzerindeki lokal deyisiklikleri itirmeden yeni branch yaradir
ve seni hemin branch-e kecirir.

### 2. Status yoxla
```bash
git status
```

Burada diqqet et:
- `.env` commit olunmamalidir
- `token.md` commit olunmamalidir

### 3. Stage et
```bash
git add apps/user/tests.py
git add apps/user/views.py
git add apps/user/serializers.py
git add apps/user/urls.py
git add core/urls.py
git add core/tests.py
git add utils/response.py
git add utils/exceptions.py
git add utils/pagination.py
git add Progress.md
git add GIT_WORKFLOW.md
git add .gitignore
```

### 4. Commit et
```bash
git commit -m "feat(users): implement tasks 7-11 for users module"
```

Istersense bunu 2 commit-e de bolmek olar:

```bash
git commit -m "feat(users): add filtering, upload and response handling"
git commit -m "docs(api): add swagger docs and workflow notes"
```

Ama minimum olaraq bir temiz commit kifayetdir.

### 5. Remote-a push et
```bash
git push -u origin feature/users
```

### 6. Pull Request ac
PR acarken:
- Base branch: `main`
- Compare branch: `feature/users`

## PR description ucun qisa format

### Edilen isler
- Task 7: users ucun filter, search, pagination
- Task 8: avatar upload
- Task 9: standard response ve global exception handling
- Task 10: minimal performance optimization
- Task 11: Swagger docs `/api/docs`

### Test
- `..\venv\Scripts\python.exe manage.py test apps.user.tests core.tests`

### Qalan hisseler
- Task 8 Postman testi
- Task 9 Postman testi
- Task 11 browser yoxlamasi
- `products` modulu hazir olanda eyni strukturun oraya tetbiqi

## Code review zamani baxilacaq hisseler
- Endpoint contract frontend ile uyqundurmu
- Response formati vahiddirmi
- Validation mesajlari aydindirmi
- Docs `/api/docs` dogru acilirmi
- Sensitive fayllar commit olunmayibmi

## Merge conflict olduqda
Eger bu vaxt diger developer `main`-e nese merge ederse:

```bash
git fetch origin
git switch feature/users
git merge origin/main
```

Sonra conflict olan fayllar hell olunur, testler yeniden isledilir:

```bash
..\venv\Scripts\python.exe manage.py test apps.user.tests core.tests
```

Sonra yeniden push:

```bash
git push
```

## Vacib qeyd
- `main` branch-ine birbasha commit etmek tavsiye olunmur.
- `.env` ve `token.md` kimi lokal ve sensitive fayllar remote-a gonderilmemelidir.
- `Task 1-6` tamamlandiqdan sonra bu branch yeniden `main` ile inteqrasiya baximindan yoxlanmalidir.
