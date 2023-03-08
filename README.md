# TP2 Qualité de code et CI/CD
Lors de  la réalisation d'un projet, il est important de pouvoir maintenir un code de bonne qualité et de faire en sorte que chacunes de vos contributions au projet soit le plus propre possible.
C'est dans cette optique que les outils Continous Integration (CI) et de Continous Delivery (CD) ont été créé.
Ensemble ils forment ce qu'on appelle le CI/CD, un set d'outils pour automatiquement tester, builder et déployer vos projets entre autres.

Dans ce TP, nous allons découvrir et utiliser les outils suivants:
- Les GitHub Actions (outils de CI/CD)
- SonarCloud (Qualité de code)
- GitLab CI/CD

## Structure du dossier TP2
    ├── README.md
    ├── src                                     <- Application à tester
    │   |
    │   └── __init__.py
    |   └── wallet.py                           <- Module gestion d'un porte-monnaie
    │
    ├── controller
    │   └── fixtures
    │       └── __init__.py
    │       └── controller.py                   <- Module de webapp
    │
    ├── tests
    │   └── fixtures
    │   |   └── __init__.py
    │   │   └── numpy_fixtures.py
    │   │   └── wallet_fixtures.py
    │   |
    │   └── unit
    │       └── __init__.py
    │       └── test_wallet.py                  <- Tests unitaires pour la librairies wallet.py
    │
    ├── .coveragerc                             <- Fichier de configuration du coverage
    ├── .gitignore
    ├── .pre-commit-config.yaml                 <- Fichier de configuration de pre-commit
    ├── .gitlab-ci.yml                          <- Fichier de configuration de Gitlab CI/CD
    ├── Dockerfile                              <- Fichier de creation d'image Docker
    └── requirements.txt

## Exercice 1: GitHub Actions
Le but de cet exercice est de vous faire découvrir les outils CI/CD de GitHub.
Si vous n'en avez pas déjà un, créez un compte sur [le site de GitHub](https://GitHub.com/).

### a)
Une fois connecté sur GitHub, créez un nouveau répository, donnez-lui un nom et laissez les autres paramètres par défaut.
Veillez à ce que le repository soit bien public et non privé. Dans le cas contraire, vous serez bloqué pour l'exercice 2.

Copiez ensuite le contenu du dossier `TP2` dans le nouveau repo en suivant ces étapes:
- Clonez votre nouveau repo
- Copiez le contenu du dossier TP2 dans le repository
- Mettez à jour votre repository avec les commandes usuelles de git

Arrivé à cette étape, vous devriez posséder un repository GitHub dont le contenu est une copie exacte de ce TP.

### b)
Vous allez créer maintenant votre première action. Rendez-vous sur la page de votre projet GitHub et cliquez sur le menu "Actions". Cliquez ensuite sur le bouton "New workflow".

![Menu action de GitHub](public/images/action_menu.png)

GitHub vous propose diverses actions prédéfinies, choisissez "Python application" et cliquez sur *Configure*.
Si cette action ne vous est pas directement proposée, vous pouvez utiliser la barre de recherche.
GitHub s'occupe de créer le fichier `python-app.yml` et de le remplir.
Analysez son contenu et répondez aux questions.

**Quelles étapes sont réalisées par cette action ?**
**Réponse:** <Entrez_votre_réponse>

**Une étape est définie au minimum par 2 paramètres, lesquels et à quoi servent-ils ?**
**Réponse:** <Entrez_votre_réponse>

**La premiète étape contient un paramètre 'with', a quoi sert ce paramètre ?**
**Réponse:** <Entrez_votre_réponse>

Vous pouvez maintenant cliquer sur "Start Commit" et "Commit new file" pour créer un nouveau commit et pousser votre nouvelle action dans le repo.
En retournant dans le menu "Actions", vous pouvez maintenant voir que le push a déclenché votre action et qu'elle est en train de s'exécuter.
Utilisez la commande `git pull` sur votre repo local et constatez qu'un nouveau fichier `python-app.yml` s'est créé dans le dossier `.github\workflows`.
C'est dans ce dossier que vous trouverez tous les fichiers de configuration de vos actions.

### c)
Vous allez maintenant modifier le fichier `python-app.yml` pour créer une action un peu plus complexe. Actuellement, votre fichier ne contient qu'un seul job nommé *build*.
Un job, dans le cadre des Actions GitHub, est une série d'étapes effectués par le même runner.Il est possible d'en avoir plusieurs par action et c'est ce que nous allons faire ici.

Ajoutez ce nouveau morceau de code à la fin du fichier.
Il s'agit d'un nouveau job qui va s'occuper de créer une image docker du projet et la pousser sur le container registry de votre compte GitHub.
Faites attention à l'indentation, `docker-image` doit être au même niveau que `build`.

```yaml

docker-image:

    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3
    - name: Login to registry
    run: echo ${{ secrets.PERSONAL_TOKEN }} | docker login ghcr.io -u <username> --password-stdin
    - name: Build the Docker image
    run: docker build . --file Dockerfile --tag ghcr.io/<username>/tp2:latest
    - name: Push the image into the registry
    run: docker push ghcr.io/<username>/tp2:latest

```

Avant de pousser vos modifications sur le repository, 2 choses sont à faire.
- Le code ci-dessus contient des balises <username>, remplacez-les par votre nom d'utilisateur GitHub.
- Créez un Personal token. Ce dernier permet au runner qui exécutera l'action d'avoir les droits d'accès à votre container registry.

Pour ce deuxième point, il suffit de vous rendre dans les paramètres de votre compte GitHub sous `Settings > Developer settings > Personal access tokens`.
Cliquez sur "Tokens (classic)" puis sur "Generate new token". Donner lui une description et les droits d'accès aux packages, comme montré ci-dessous

![GitHub personal access token scope](public/images/github_token_scope.png)

Cliquez ensuite sur "Generate token" en bas de la page. Copiez le token généré et notez le quelque part, vous ne pourrez plus y avoir accès une fois la page quittée.
Rendez-vous ensuite sur la page de votre repository et alez sous `Settings > Secrets and variables > Actions`.
Créez un nouveau secret en cliquant sur "New repository secret". Nommez le "PERSONAL_TOKEN" et entrez votre token comme valeur.

Une fois cela fait, tout devrait marcher. Vous pouvez maintenant poussez vos modifications sur le repository et observer votre action s'exécuter.

## Exercice 2: Qualité de code
Dans le TP1 nous avions vu l'outil pre-commit qui permet d'appliquer, entre autres, des règles de formatage à votre code avant de le pousser sur le repo.
Ici nous allons aller plus loin grâce à l'outil SonarQube. Ce dernier permet, en le combinant avec le CI/CD, d'analyser votre code en profondeur à chaque fois que vous faites un push.
Ainsi, vous pouvez rapidement voir si votre code contient des problèmes de maintenabilité, sécurité, etc...
SonarQube possède une version cloud, SonarCloud, qui offre les mêmes capacités sans devoir se soucier de la gestion du serveur.
C'est cette version que nous allons utiliser dans ce TP.

### a)
Pour commencer, il faut lier votre compte GitHub à SonarCloud. Pour ce faire, allez sur [la page de connexion de SonarCloud](https://sonarcloud.io/login) et choisissez la connexion via GitHub.
SonarCloud va vous guider pour lier votre compte et choisir un repo à analyser. Séléctionnez le repo que vous avez créé pour l'exercice 1.
Le processus devrait être facile et en quelques minutes vous pourrez voir la 1ère analyse du projet.

Une analyse de code va maintenant se lancer à chaque push et vous pourrez voir les résultats depuis le tableau de bord de SonarCloud.

**Sur l'onglet Summary d'une analyse de code, SonarCloud fournit 4 indicateurs. Quels sont-ils et quels sont leurs utilités ?**

**Réponse:** <Entrez_votre_réponse>

### b)
Par défaut SonarCloud s'occupe de faire la connexion avec votre projet GitHub automatiquement.
C'est certes très pratique mais cette méthode ne permet pas de personnaliser la configuration, ce qui nous prive de certaines fonctionnalités.
Vous allez donc modifier la méthode de connexion entre GitHub et SonarCloud et ajouter l'analyse du coverage.

Depuis le tableau de bord du projet sur SonarCloud, rendez-vous sur `Administration > Analysis Method`.
Décochez "Automatic Analysis" et suivez le tutorial "GitHub Actions".
Ce dernier vous propose une étape **Create or update a build file** pour créer une nouvelle action.
Vous pouvez ignorer cette étape, à la place vous allez simplement modifier le fichier `python-app.yml` qui existe déjà dans le répértoire de votre projet.
Modifiez le job *build* comme suit. Les modifications sont commentées pour mieux vous rendre compte des changements.

```yaml
build:

    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3
    - name: Set up Python 3.10
      uses: actions/setup-python@v3
      with:
        python-version: "3.10"
        fetch-depth: 0 # fetch all history for all branches and tags
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install flake8 pytest
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
    - name: Lint with flake8
      run: |
        # stop the build if there are Python syntax errors or undefined names
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        # exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
        flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
    - name: Test with pytest # Using --cov=. --cov-report=xml to create a coverage and export it as an xml file
      run: |
        pytest --cov=. --cov-report=xml
    - name: SonarCloud Scan # Add a SonarCloud Scan step to make the connection with SonarCloud
      uses: SonarSource/sonarcloud-github-action@master
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

Pour finir, il vous reste encore à indiquer à SonarCloud où trouver le fichier de coverage.
Pour ça, il suffit d'ajouter les lignes suivantes au fichier `sonar-project.properties`.
Notez que la deuxième ligne indique à SonarCloud d'ignorer certains dossiers/fichiers pour le calcul du coverage. Sans ça, tous les fichiers Python sont considérés.

```
sonar.python.coverage.reportPaths=coverage.xml
sonar.coverage.exclusions=**/tests/**,**/controller/**,setup.py
```

Une fois tout ça fait, vous pouvez pousser les modifications sur le repository. L'action GitHub va se lancer et suite à ça l'analyse SonarCloud.
Vous devriez maintenant avoir accès au coverage.
Allez sur l'onglet "Summary" du projet SonarCloud, cliquez sur le bouton "Overall Code" et répondez aux questions.

**Quelle est la différence entre les sections 'New code' et 'Overall Code' dans l'onglet Summary ?**

**Réponse:** <Entrez_votre_réponse>

**Y a-t-il des Code Smells ? Si oui, combien et pour quelle(s) raisons(s) ?**

**Réponse:** <Entrez_votre_réponse>

**Y a-t-il des Security Hotspots ? Si oui, combien et pour quelle(s) raison(s) ?**

**Réponse:** <Entrez_votre_réponse>

### c)

Maintenant que vous savez quelles erreurs se sont glissées dans le code, modifiez le pour enlever les Code Smells et Security Hotspots.
SonarCloud est assez puissant pour comprendre les erreurs et vous proposer des solutions, n'hésitez pas à parcourir les sections du tableau de bord.
Une fois fini, poussez vos modifications sur le repository. L'analyse de code ne devraient plus indiquer d'erreur.

## Exercice 3: Gitlab CI/CD

**Question pour Fabrizio** Sous quelle forme les élèves reçoivent-ils le TP ? Un zip ? un repo ?
Suivant la réponse -> Préciser dans la consigne de créer un repo GitLab sur la forge étudiante et copier le contenu du tp dedans pour ensuite pouvoir tester les effets du fichier yaml.


Pour finir, vous allez utilisez le fichier `.gitlab-ci.yml` proposé à la racine de ce projet.
Tout comme GitHub, Gitlab offre la possibilité des outils de CI/CD configurables à partir de fichiers yaml.
Un fichier définit une [Pipeline](https://docs.gitlab.com/ee/ci/pipelines/) et cette dernière contient un ou plusieurs stages.
Analysez le contenu du fichier `.gitlab-ci.yml` et testez ses effets en poussant des modifications sans importance sur le repository Gitlab (en ajoutant un commentaire par exemple).
Répondez ensuite aux questions.

**Cette Pipeline contient 3 stages. Quels sont leur nom ?**

**Réponse:** <Entrez_votre_réponse>

**Que fait le premier stage ?**

**Réponse:** <Entrez_votre_réponse>

**Que fait le deuxième stage ?**

**Réponse:** <Entrez_votre_réponse>

**Que fait le troisième stage ?**

**Réponse:** <Entrez_votre_réponse>

**Le stage 2 génère une Image docker. Qu'est-ce que c'est et où pouvez-vous le retrouver ?**

**Réponse:** <Entrez_votre_réponse>

**Le stage 3 génère une wheel Python. Qu'est-ce que c'est et où pouvez-vous la retrouver ?**

**Réponse:** <Entrez_votre_réponse>
