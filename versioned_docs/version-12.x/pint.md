# Laravel Pint (Laravel Pint)

- [소개](#introduction)
- [설치](#installation)
- [Pint 실행](#running-pint)
- [Pint 설정](#configuring-pint)
    - [프리셋](#presets)
    - [규칙](#rules)
    - [파일/폴더 제외](#excluding-files-or-folders)
- [지속적 통합(CI)](#continuous-integration)
    - [GitHub Actions](#running-tests-on-github-actions)

<a name="introduction"></a>
## 소개

[Laravel Pint](https://github.com/laravel/pint)는 미니멀리스트를 위한 명확한 기준의 PHP 코드 스타일 자동 정리 도구입니다. Pint는 [PHP CS Fixer](https://github.com/FriendsOfPHP/PHP-CS-Fixer)를 기반으로 하며, 코드 스타일이 항상 깔끔하고 일관되게 유지되도록 손쉽게 도와줍니다.

Pint는 모든 신규 Laravel 애플리케이션에 자동으로 포함되어 있으므로 즉시 사용할 수 있습니다. 기본적으로 별도의 설정 없이도 동작하며, Laravel의 견해를 반영한 코드 스타일을 따라 코드 내의 스타일 문제를 자동으로 수정합니다.

<a name="installation"></a>
## 설치

Pint는 최근 릴리즈된 Laravel 프레임워크에 기본 포함되어 있으므로 일반적으로 별도 설치가 필요하지 않습니다. 그러나 구버전 애플리케이션에서는 Composer를 통해 Laravel Pint를 설치할 수 있습니다:

```shell
composer require laravel/pint --dev
```

<a name="running-pint"></a>
## Pint 실행

Pint로 코드 스타일 문제를 수정하려면, 프로젝트의 `vendor/bin` 디렉터리에 있는 `pint` 바이너리를 실행하면 됩니다:

```shell
./vendor/bin/pint
```

성능 향상을 위해 Pint를 병렬(parallel) 모드(실험적)로 실행하고 싶다면, `--parallel` 옵션을 사용할 수 있습니다:

```shell
./vendor/bin/pint --parallel
```

병렬 모드에서는 추가로 `--max-processes` 옵션을 통해 동시에 실행할 최대 프로세스 수를 지정할 수 있습니다. 옵션을 지정하지 않으면 Pint는 시스템의 모든 사용 가능한 코어를 사용합니다:

```shell
./vendor/bin/pint --parallel --max-processes=4
```

또한 특정 파일이나 디렉터리에만 Pint를 실행할 수도 있습니다:

```shell
./vendor/bin/pint app/Models

./vendor/bin/pint app/Models/User.php
```

Pint는 업데이트된 모든 파일의 상세 목록을 출력합니다. 변경 내역을 더 자세히 보고 싶다면, `-v` 옵션을 추가하여 실행할 수 있습니다:

```shell
./vendor/bin/pint -v
```

Pint가 실제로 파일을 변경하지 않고, 코드 스타일 오류만 검사하도록 하려면 `--test` 옵션을 사용할 수 있습니다. 코드 스타일 오류가 발견되면 Pint는 0이 아닌 종료 코드를 반환합니다:

```shell
./vendor/bin/pint --test
```

Git 기준으로 지정한 브랜치와 다른 파일만 Pint가 수정하도록 하려면, `--diff=[branch]` 옵션을 사용할 수 있습니다. 이는 CI 환경(GitHub Actions 등)에서 새로운 파일이나 변경된 파일만 검사하여 시간을 절약하는 데 효과적입니다:

```shell
./vendor/bin/pint --diff=main
```

또한 Git에서 커밋되지 않은 변경이 있는 파일만 Pint가 수정하도록 하려면 `--dirty` 옵션을 사용할 수 있습니다:

```shell
./vendor/bin/pint --dirty
```

코드 스타일 오류가 있는 파일을 수정하되, 오류를 수정한 경우에는 0이 아닌 종료 코드로 종료하도록 하려면 `--repair` 옵션을 사용할 수 있습니다:

```shell
./vendor/bin/pint --repair
```

<a name="configuring-pint"></a>
## Pint 설정

앞서 언급했듯, Pint는 별도의 설정 없이도 사용할 수 있습니다. 하지만 프리셋(preset), 규칙(rules), 검사할 폴더를 커스텀하고 싶다면, 프로젝트 루트 디렉터리에 `pint.json` 파일을 생성해 원하는 대로 설정할 수 있습니다:

```json
{
    "preset": "laravel"
}
```

또한 특정 디렉터리에 있는 `pint.json` 파일을 사용하려면, Pint 실행 시 `--config` 옵션을 추가로 제공할 수 있습니다:

```shell
./vendor/bin/pint --config vendor/my-company/coding-style/pint.json
```

<a name="presets"></a>
### 프리셋

프리셋(preset)은 코드 스타일을 자동으로 맞춰줄 규칙들의 집합을 의미합니다. 기본적으로 Pint는 `laravel` 프리셋을 사용하며, 이 설정은 Laravel의 코드 스타일을 기준으로 스타일 문제를 자동 정리합니다. 다른 프리셋을 사용하고 싶다면 Pint 실행 시 `--preset` 옵션을 통해 지정할 수 있습니다:

```shell
./vendor/bin/pint --preset psr12
```

또는, 프로젝트의 `pint.json` 파일에서 프리셋을 지정해줄 수도 있습니다:

```json
{
    "preset": "psr12"
}
```

현재 Pint가 지원하는 프리셋은 다음과 같습니다: `laravel`, `per`, `psr12`, `symfony`, `empty`.

<a name="rules"></a>
### 규칙

규칙(rule)은 Pint가 코드 스타일을 자동으로 수정할 때 적용하는 세부 지침입니다. 앞서 설명한 대로, 프리셋에는 보통 PHP 프로젝트에 적합한 규칙들이 미리 지정되어 있으므로, 개별 규칙을 신경 쓰지 않아도 됩니다.

그러나 원하는 경우, 프로젝트의 `pint.json` 파일에서 특정 규칙을 직접 활성화하거나 비활성화할 수 있으며, 또는 `empty` 프리셋으로 시작해서 원하는 규칙만 직접 추가할 수도 있습니다:

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

Pint는 [PHP CS Fixer](https://github.com/FriendsOfPHP/PHP-CS-Fixer) 위에 구축되어 있으므로, PHP CS Fixer의 모든 규칙을 사용할 수 있습니다: [PHP CS Fixer Configurator](https://mlocati.github.io/php-cs-fixer-configurator).

<a name="excluding-files-or-folders"></a>
### 파일/폴더 제외

기본적으로 Pint는 프로젝트 내의 모든 `.php` 파일을 검사하지만, `vendor` 디렉터리 내부는 제외합니다. 더 많은 폴더를 제외하고 싶다면, `exclude` 설정 옵션을 사용할 수 있습니다:

```json
{
    "exclude": [
        "my-specific/folder"
    ]
}
```

특정 이름 패턴을 가진 파일 모두를 제외하려면, `notName` 옵션을 쓸 수 있습니다:

```json
{
    "notName": [
        "*-my-file.php"
    ]
}
```

정확한 경로를 지정해서 파일 하나만 제외하려면, `notPath` 옵션을 사용할 수 있습니다:

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

Laravel Pint로 프로젝트 린트(코드 스타일 검사)를 자동화하려면 [GitHub Actions](https://github.com/features/actions)를 구성하여 새 코드가 GitHub에 push될 때마다 Pint를 실행할 수 있습니다. 먼저 GitHub의 **Settings > Actions > General > Workflow permissions**에서 워크플로우에 "Read and write permissions" 권한을 부여하세요. 그런 다음 다음과 같이 `.github/workflows/lint.yml` 파일을 생성하세요:

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
