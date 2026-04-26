# Laravel Pint (Laravel Pint)

- [소개](#introduction)
- [설치](#installation)
- [Pint 실행하기](#running-pint)
- [Pint 설정하기](#configuring-pint)
    - [프리셋](#presets)
    - [규칙](#rules)
    - [파일 / 폴더 제외](#excluding-files-or-folders)
- [지속적 통합](#continuous-integration)
    - [GitHub Actions](#running-tests-on-github-actions)

<a name="introduction"></a>
## 소개 (Introduction)

[Laravel Pint](https://github.com/laravel/pint)는 간결함을 선호하는 개발자를 위한 의견이 반영된 PHP 코드 스타일 수정 도구입니다. Pint는 [PHP CS Fixer](https://github.com/FriendsOfPHP/PHP-CS-Fixer)를 기반으로 만들어졌으며, 코드 스타일을 깔끔하고 일관되게 유지하기 쉽게 해줍니다.

Pint는 새 Laravel 애플리케이션에 자동으로 설치되므로 바로 사용할 수 있습니다. 기본적으로 Pint는 별도의 설정이 필요하지 않으며, Laravel의 의견이 반영된 코딩 스타일을 따라 코드의 스타일 문제를 수정합니다.

<a name="installation"></a>
## 설치 (Installation)

Pint는 최근 Laravel 프레임워크 릴리스에 포함되어 있으므로 일반적으로 별도 설치가 필요하지 않습니다. 하지만 오래된 애플리케이션에서는 Composer를 통해 Laravel Pint를 설치할 수 있습니다.

```shell
composer require laravel/pint --dev
```

<a name="running-pint"></a>
## Pint 실행하기 (Running Pint)

프로젝트의 `vendor/bin` 디렉터리에 있는 `pint` 바이너리를 실행하여 Pint가 코드 스타일 문제를 수정하도록 할 수 있습니다.

```shell
./vendor/bin/pint
```

성능 향상을 위해 Pint를 병렬 모드(실험적 기능)로 실행하려면 `--parallel` 옵션을 사용할 수 있습니다.

```shell
./vendor/bin/pint --parallel
```

병렬 모드에서는 `--max-processes` 옵션으로 실행할 최대 프로세스 수를 지정할 수도 있습니다. 이 옵션을 제공하지 않으면 Pint는 사용 중인 머신에서 사용 가능한 모든 코어를 사용합니다.

```shell
./vendor/bin/pint --parallel --max-processes=4
```

특정 파일이나 디렉터리에 대해서만 Pint를 실행할 수도 있습니다.

```shell
./vendor/bin/pint app/Models

./vendor/bin/pint app/Models/User.php
```

Pint는 업데이트한 모든 파일의 상세 목록을 표시합니다. Pint가 변경한 내용을 더 자세히 보려면 Pint를 실행할 때 `-v` 옵션을 제공하면 됩니다.

```shell
./vendor/bin/pint -v
```

파일을 실제로 변경하지 않고 코드에 스타일 오류가 있는지만 검사하려면 `--test` 옵션을 사용할 수 있습니다. 코드 스타일 오류가 발견되면 Pint는 0이 아닌 종료 코드를 반환합니다.

```shell
./vendor/bin/pint --test
```

Git 기준으로 제공한 브랜치와 다른 파일만 Pint가 수정하도록 하려면 `--diff=[branch]` 옵션을 사용할 수 있습니다. 이 옵션은 GitHub Actions 같은 CI 환경에서 새 파일이나 수정된 파일만 검사하여 시간을 절약하는 데 효과적으로 사용할 수 있습니다.

```shell
./vendor/bin/pint --diff=main
```

Git 기준으로 커밋되지 않은 변경 사항이 있는 파일만 Pint가 수정하도록 하려면 `--dirty` 옵션을 사용할 수 있습니다.

```shell
./vendor/bin/pint --dirty
```

코드 스타일 오류가 있는 파일을 수정하되, 오류가 수정된 경우 0이 아닌 종료 코드로 종료되도록 하려면 `--repair` 옵션을 사용할 수 있습니다.

```shell
./vendor/bin/pint --repair
```

<a name="configuring-pint"></a>
## Pint 설정하기 (Configuring Pint)

앞서 언급했듯이 Pint는 별도의 설정이 필요하지 않습니다. 하지만 프리셋, 규칙 또는 검사할 폴더를 사용자 정의하려면 프로젝트 루트 디렉터리에 `pint.json` 파일을 만들면 됩니다.

```json
{
    "preset": "laravel"
}
```

또한 특정 디렉터리에 있는 `pint.json`을 사용하려면 Pint를 실행할 때 `--config` 옵션을 제공할 수 있습니다.

```shell
./vendor/bin/pint --config vendor/my-company/coding-style/pint.json
```

<a name="presets"></a>
### 프리셋

프리셋은 코드의 스타일 문제를 수정하는 데 사용할 수 있는 규칙 집합을 정의합니다. 기본적으로 Pint는 Laravel의 의견이 반영된 코딩 스타일을 따라 문제를 수정하는 `laravel` 프리셋을 사용합니다. 하지만 Pint에 `--preset` 옵션을 제공하여 다른 프리셋을 지정할 수 있습니다.

```shell
./vendor/bin/pint --preset psr12
```

원한다면 프로젝트의 `pint.json` 파일에서 프리셋을 설정할 수도 있습니다.

```json
{
    "preset": "psr12"
}
```

현재 Pint가 지원하는 프리셋은 `laravel`, `per`, `psr12`, `symfony`, `empty`입니다.

<a name="rules"></a>
### 규칙

규칙은 Pint가 코드의 스타일 문제를 수정할 때 사용하는 스타일 지침입니다. 위에서 언급했듯이 프리셋은 대부분의 PHP 프로젝트에 적합하도록 미리 정의된 규칙 그룹이므로, 일반적으로 프리셋에 포함된 개별 규칙을 신경 쓸 필요는 없습니다.

하지만 원한다면 `pint.json` 파일에서 특정 규칙을 활성화하거나 비활성화할 수 있으며, `empty` 프리셋을 사용해 규칙을 처음부터 직접 정의할 수도 있습니다.

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

Pint는 [PHP CS Fixer](https://github.com/FriendsOfPHP/PHP-CS-Fixer)를 기반으로 만들어졌습니다. 따라서 프로젝트의 코드 스타일 문제를 수정하기 위해 PHP CS Fixer의 모든 규칙을 사용할 수 있습니다. [PHP CS Fixer Configurator](https://mlocati.github.io/php-cs-fixer-configurator)를 참고하십시오.

<a name="excluding-files-or-folders"></a>
### 파일 / 폴더 제외

기본적으로 Pint는 `vendor` 디렉터리에 있는 파일을 제외하고 프로젝트의 모든 `.php` 파일을 검사합니다. 더 많은 폴더를 제외하려면 `exclude` 설정 옵션을 사용할 수 있습니다.

```json
{
    "exclude": [
        "my-specific/folder"
    ]
}
```

특정 이름 패턴을 포함하는 모든 파일을 제외하려면 `notName` 설정 옵션을 사용할 수 있습니다.

```json
{
    "notName": [
        "*-my-file.php"
    ]
}
```

파일의 정확한 경로를 제공하여 특정 파일을 제외하려면 `notPath` 설정 옵션을 사용할 수 있습니다.

```json
{
    "notPath": [
        "path/to/excluded-file.php"
    ]
}
```

<a name="continuous-integration"></a>
## 지속적 통합 (Continuous Integration)

<a name="running-tests-on-github-actions"></a>
### GitHub Actions

Laravel Pint로 프로젝트 린팅을 자동화하려면 새 코드가 GitHub에 푸시될 때마다 Pint가 실행되도록 [GitHub Actions](https://github.com/features/actions)를 설정할 수 있습니다. 먼저 GitHub의 **Settings > Actions > General > Workflow permissions**에서 워크플로에 "Read and write permissions" 권한을 부여했는지 확인하십시오. 그런 다음 다음 내용으로 `.github/workflows/lint.yml` 파일을 만드십시오.

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
