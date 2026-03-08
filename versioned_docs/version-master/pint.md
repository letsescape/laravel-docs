# Laravel Pint (Laravel Pint)

- [소개](#introduction)
- [설치](#installation)
- [Pint 실행하기](#running-pint)
- [Pint 설정하기](#configuring-pint)
    - [프리셋](#presets)
    - [규칙](#rules)
    - [파일 / 폴더 제외하기](#excluding-files-or-folders)
- [지속적 통합(CI)](#continuous-integration)
    - [GitHub Actions](#running-tests-on-github-actions)

<a name="introduction"></a>
## 소개

[Laravel Pint](https://github.com/laravel/pint)는 미니멀리스트를 위한 독단적인(의견이 강하게 반영된) PHP 코드 스타일 수정 도구입니다. Pint는 [PHP CS Fixer](https://github.com/FriendsOfPHP/PHP-CS-Fixer)를 기반으로 하며, 코드 스타일을 깨끗하고 일관되게 유지하는 작업을 아주 간단하게 만들어줍니다.

Pint는 모든 새로운 Laravel 애플리케이션에 자동으로 설치되어 있으므로 바로 사용할 수 있습니다. 기본적으로 Pint는 별도의 설정이 필요 없으며, Laravel의 독단적인(의견이 반영된) 코딩 스타일을 따라 코드 스타일 문제를 고쳐줍니다.

<a name="installation"></a>
## 설치

Pint는 최근에 릴리스된 Laravel 프레임워크에 기본 포함되어 있으므로, 일반적으로 별도의 설치가 필요하지 않습니다. 하지만 이전 애플리케이션의 경우, Composer를 통해 Laravel Pint를 설치할 수 있습니다:

```shell
composer require laravel/pint --dev
```

<a name="running-pint"></a>
## Pint 실행하기

Pint로 코드 스타일 문제를 고치려면, 프로젝트의 `vendor/bin` 디렉터리에 위치한 `pint` 실행 파일을 사용하면 됩니다:

```shell
./vendor/bin/pint
```

성능 향상을 위해 Pint를 병렬 모드(실험적)로 실행하고 싶다면, `--parallel` 옵션을 사용할 수 있습니다:

```shell
./vendor/bin/pint --parallel
```

병렬 모드에서는 `--max-processes` 옵션으로 동시에 실행할 최대 프로세스 수를 지정할 수 있습니다. 이 옵션을 생략하면, Pint는 컴퓨터의 모든 사용 가능한 코어를 사용합니다:

```shell
./vendor/bin/pint --parallel --max-processes=4
```

특정 파일이나 디렉터리만 대상으로 Pint를 실행할 수도 있습니다:

```shell
./vendor/bin/pint app/Models

./vendor/bin/pint app/Models/User.php
```

Pint는 업데이트한 모든 파일의 자세한 목록을 출력해줍니다. Pint의 변경 내역을 더 자세히 보고 싶으면, `-v` 옵션을 추가해 실행할 수 있습니다:

```shell
./vendor/bin/pint -v
```

파일을 실제로 변경하지 않고 코드 스타일 오류만 점검하려면, `--test` 옵션을 사용하세요. 코드 스타일 오류가 발견되면 Pint는 0이 아닌 종료 코드를 반환합니다:

```shell
./vendor/bin/pint --test
```

Git 기준으로 제공된 브랜치와 비교해 차이가 있는 파일만 Pint가 수정하도록 하려면, `--diff=[branch]` 옵션을 사용할 수 있습니다. 이 방법은 CI 환경(예: GitHub Actions)에서 새롭게 추가되거나 수정된 파일만 검사할 때 효과적입니다:

```shell
./vendor/bin/pint --diff=main
```

Git에 커밋되지 않은 변경사항이 있는 파일만 Pint가 수정하게 하려면, `--dirty` 옵션을 사용할 수 있습니다:

```shell
./vendor/bin/pint --dirty
```

코드 스타일 오류가 있는 파일을 고치면서 동시에 오류가 한 건이라도 고쳐졌다면 0이 아닌 종료 코드로 종료하게 하려면, `--repair` 옵션을 사용합니다:

```shell
./vendor/bin/pint --repair
```

<a name="configuring-pint"></a>
## Pint 설정하기

앞서 언급한 것처럼, Pint는 별도의 설정이 필요하지 않습니다. 하지만 프리셋, 규칙 또는 검사할 폴더를 커스터마이즈하고 싶다면, 프로젝트의 루트 디렉터리에 `pint.json` 파일을 생성해 설정할 수 있습니다:

```json
{
    "preset": "laravel"
}
```

또한, 특정 디렉터리에 있는 `pint.json` 설정 파일을 사용하고 싶을 때는, Pint를 실행할 때 `--config` 옵션으로 해당 파일 경로를 지정할 수 있습니다:

```shell
./vendor/bin/pint --config vendor/my-company/coding-style/pint.json
```

<a name="presets"></a>
### 프리셋

프리셋(preset)은 코드 스타일 문제를 해결하기 위해 사용할 규칙 모음입니다. 기본적으로 Pint는 `laravel` 프리셋을 사용하여, Laravel의 독단적인 코딩 스타일에 따라 문제를 고칩니다. 하지만 원한다면 `--preset` 옵션으로 다른 프리셋을 지정할 수 있습니다:

```shell
./vendor/bin/pint --preset psr12
```

또는 프로젝트의 `pint.json` 파일에 프리셋을 지정할 수도 있습니다:

```json
{
    "preset": "psr12"
}
```

Pint에서 현재 지원하는 프리셋은 다음과 같습니다: `laravel`, `per`, `psr12`, `symfony`, `empty`.

<a name="rules"></a>
### 규칙

규칙(rule)은 Pint가 코드 스타일 문제를 고칠 때 따르는 세부 스타일 지침입니다. 앞서 설명한 대로, 프리셋은 대부분의 PHP 프로젝트에 적합하도록 미리 정의된 규칙 그룹이기 때문에, 보통 개별 규칙을 신경 쓸 필요는 없습니다.

하지만 필요하다면, `pint.json` 파일에서 특정 규칙을 개별적으로 활성화(Enable)하거나 비활성화(Disable)할 수 있고, `empty` 프리셋을 활용해 처음부터 직접 규칙을 설정할 수도 있습니다:

```json
{
    "preset": "laravel",
    "rules": {
        "simplified_null_return": true,
        "array_indentation": false,
        "new_with_parentheses": {
            "anonymous_class": true,
            "named_class": true
        }
    }
}
```

Pint는 [PHP CS Fixer](https://github.com/FriendsOfPHP/PHP-CS-Fixer)를 기반으로 만들어졌으므로, 여기에 정의된 모든 규칙을 사용할 수 있습니다: [PHP CS Fixer Configurator](https://mlocati.github.io/php-cs-fixer-configurator).

<a name="excluding-files-or-folders"></a>
### 파일 / 폴더 제외하기

기본적으로 Pint는 `vendor` 디렉터리를 제외한 프로젝트의 모든 `.php` 파일을 검사합니다. 만약 추가로 제외하고 싶은 폴더가 있다면, `exclude` 옵션으로 설정할 수 있습니다:

```json
{
    "exclude": [
        "my-specific/folder"
    ]
}
```

특정 이름 패턴을 포함하는 모든 파일을 제외하고 싶다면, `notName` 옵션을 사용할 수 있습니다:

```json
{
    "notName": [
        "*-my-file.php"
    ]
}
```

정확한 파일 경로를 지정하여 파일을 제외하고 싶다면, `notPath` 옵션을 사용할 수 있습니다:

```json
{
    "notPath": [
        "path/to/excluded-file.php"
    ]
}
```

<a name="continuous-integration"></a>
## 지속적 통합(CI)

<a name="running-tests-on-github-actions"></a>
### GitHub Actions

Laravel Pint로 프로젝트 린트(lint)를 자동화하려면, [GitHub Actions](https://github.com/features/actions)를 설정해 새로운 코드가 GitHub에 푸시될 때마다 Pint가 실행되도록 할 수 있습니다. 먼저, GitHub 내 **Settings > Actions > General > Workflow permissions**에서 워크플로우에 "Read and write permissions(읽기 및 쓰기 권한)"을 부여해야 합니다. 그 다음, 아래와 같이 `.github/workflows/lint.yml` 파일을 만들어주세요:

```yaml
name: Fix Code Style

on: [push]

jobs:
  lint:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: true
      matrix:
        php: [8.4]

    steps:
      - name: Checkout code
        uses: actions/checkout@v5

      - name: Setup PHP
        uses: shivammathur/setup-php@v2
        with:
          php-version: ${{ matrix.php }}
          tools: pint

      - name: Run Pint
        run: pint

      - name: Commit linted files
        uses: stefanzweifel/git-auto-commit-action@v6
```