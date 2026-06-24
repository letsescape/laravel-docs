<!-- # Laravel Pint -->
# Laravel Pint

- [Introduction](#introduction)
- [Installation](#installation)
- [Running Pint](#running-pint)
- [Configuring Pint](#configuring-pint)
    - [Presets](#presets)
    - [Rules](#rules)
    - [Excluding Files / Folders](#excluding-files-or-folders)
- [Continuous Integration](#continuous-integration)
    - [GitHub Actions](#running-tests-on-github-actions)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- [Laravel Pint](https://github.com/laravel/pint) is an opinionated PHP code style fixer for minimalists. Pint is built on top of PHP-CS-Fixer and makes it simple to ensure that your code style stays clean and consistent. -->
[Laravel Pint](https://github.com/laravel/pint)는 미니멀리스트(최소주의자)를 위한 Laravel의 의견이 반영된 PHP 코드 스타일 수정 도구입니다. Pint는 PHP-CS-Fixer 위에 구축되어 있으며, 코드 스타일을 항상 깔끔하고 일관되게 유지할 수 있도록 간편하게 도와줍니다.

<!-- Pint is automatically installed with all new Laravel applications so you may start using it immediately. By default, Pint does not require any configuration and will fix code style issues in your code by following the opinionated coding style of Laravel. -->
Pint는 새로운 Laravel 애플리케이션에 자동으로 설치되므로, 바로 사용할 수 있습니다. 기본적으로 Pint는 별도의 설정이 필요하지 않으며, Laravel에서 권장하는 코드 스타일을 따라 코드 내 스타일 문제를 자동으로 수정합니다.

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- Pint is included in recent releases of the Laravel framework, so installation is typically unnecessary. However, for older applications, you may install Laravel Pint via Composer: -->
Pint는 최신 Laravel 프레임워크 릴리스에 기본 포함되어 있으므로, 별도의 설치가 필요 없는 경우가 많습니다. 다만, 구버전 애플리케이션에서는 Composer를 통해 Laravel Pint를 설치할 수 있습니다.

```shell
composer require laravel/pint --dev
```

<a name="running-pint"></a>
<!-- ## Running Pint -->
## Running Pint

<!-- You can instruct Pint to fix code style issues by invoking the `pint` binary that is available in your project's `vendor/bin` directory: -->
Pint를 사용하여 코드 스타일 문제를 자동으로 수정하려면, 프로젝트의 `vendor/bin` 디렉터리에 있는 `pint` 실행 파일을 다음과 같이 실행합니다.

```shell
./vendor/bin/pint
```

<!-- You may also run Pint on specific files or directories: -->
특정 파일이나 디렉터리만 대상으로 Pint를 실행할 수도 있습니다.

```shell
./vendor/bin/pint app/Models

./vendor/bin/pint app/Models/User.php
```

<!-- Pint will display a thorough list of all of the files that it updates. You can view even more detail about Pint's changes by providing the `-v` option when invoking Pint: -->
Pint는 수정된 모든 파일 목록을 상세하게 보여줍니다. `-v` 옵션을 함께 사용하면 Pint가 적용한 변경 사항을 더 자세히 확인할 수 있습니다.

```shell
./vendor/bin/pint -v
```

<!-- If you would like Pint to simply inspect your code for style errors without actually changing the files, you may use the `--test` option. Pint will return a non-zero exit code if any code style errors are found: -->
파일을 실제로 변경하지 않고, 코드 스타일 오류만 점검하고 싶다면 `--test` 옵션을 사용할 수 있습니다. 스타일 오류가 발견되면 Pint는 0이 아닌 종료 코드를 반환합니다.

```shell
./vendor/bin/pint --test
```

<!-- If you would like Pint to only modify the files that differ from the provided branch according to Git, you may use the `--diff=[branch]` option. This can be effectively used in your CI environment (like GitHub actions) to save time by only inspecting new or modified files: -->
Git 상의 특정 브랜치와 비교하여 변경된 파일(새로 생성되었거나 수정된 파일)만 검사하고 싶을 때는 `--diff=[branch]` 옵션을 사용할 수 있습니다. 이 옵션은 GitHub Actions와 같은 CI 환경에서 시간 단축에 효과적입니다.

```shell
./vendor/bin/pint --diff=main
```

<!-- If you would like Pint to only modify the files that have uncommitted changes according to Git, you may use the `--dirty` option: -->
Git에서 커밋되지 않은 변경 사항이 있는 파일만 검사하려면 `--dirty` 옵션을 사용합니다.

```shell
./vendor/bin/pint --dirty
```

<!-- If you would like Pint to fix any files with code style errors but also exit with a non-zero exit code if any errors were fixed, you may use the `--repair` option: -->
Pint가 코드 스타일 문제를 찾아서 고치되, 하나라도 수정된 파일이 있다면 0이 아닌 종료 코드로 종료되게 하려면 `--repair` 옵션을 사용할 수 있습니다.

```shell
./vendor/bin/pint --repair
```

<a name="configuring-pint"></a>
<!-- ## Configuring Pint -->
## Configuring Pint

<!-- As previously mentioned, Pint does not require any configuration. However, if you wish to customize the presets, rules, or inspected folders, you may do so by creating a `pint.json` file in your project's root directory: -->
앞서 설명했듯이 Pint는 별도의 설정 없이 바로 사용할 수 있습니다. 그러나 프리셋, 룰, 검사할 폴더 등을 직접 설정하고 싶다면, 프로젝트의 루트 디렉터리에 `pint.json` 파일을 만들어 설정할 수 있습니다.

```json
{
    "preset": "laravel"
}
```

<!-- In addition, if you wish to use a `pint.json` from a specific directory, you may provide the `--config` option when invoking Pint: -->
또한, 특정 디렉터리에 있는 `pint.json` 설정 파일을 사용하려면 Pint 실행 시 `--config` 옵션을 지정하면 됩니다.

```shell
./vendor/bin/pint --config vendor/my-company/coding-style/pint.json
```

<a name="presets"></a>
<!-- ### Presets -->
### Presets

<!-- Presets define a set of rules that can be used to fix code style issues in your code. By default, Pint uses the `laravel` preset, which fixes issues by following the opinionated coding style of Laravel. However, you may specify a different preset by providing the `--preset` option to Pint: -->
프리셋(preset)은 코드 스타일 문제를 수정할 때 사용할 룰 세트를 정의합니다. 기본적으로 Pint는 `laravel` 프리셋을 사용하며, Laravel이 권장하는 코드 스타일로 코드를 고쳐줍니다. 다른 프리셋을 사용하려면 Pint 실행 시 `--preset` 옵션으로 지정할 수 있습니다.

```shell
./vendor/bin/pint --preset psr12
```

<!-- If you wish, you may also set the preset in your project's `pint.json` file: -->
원한다면 프로젝트의 `pint.json` 파일에도 프리셋을 직접 설정할 수 있습니다.

```json
{
    "preset": "psr12"
}
```

<!-- Pint's currently supported presets are: `laravel`, `per`, `psr12`, `symfony`, and `empty`. -->
현재 Pint에서 지원하는 프리셋은 다음과 같습니다: `laravel`, `per`, `psr12`, `symfony`, `empty`.

<a name="rules"></a>
<!-- ### Rules -->
### Rules

<!-- Rules are style guidelines that Pint will use to fix code style issues in your code. As mentioned above, presets are predefined groups of rules that should be perfect for most PHP projects, so you typically will not need to worry about the individual rules they contain. -->
룰(rule)은 Pint가 코드 스타일 문제를 수정할 때 따르는 세부 기준(스타일 가이드라인)입니다. 앞서 안내한 것처럼 프리셋은 여러 룰을 미리 묶어둔 것으로, 대부분의 PHP 프로젝트에는 프리셋만으로 충분히 적합하게 스타일을 맞출 수 있습니다. 따라서 일반적으로 개별 룰을 신경 쓰지 않아도 괜찮습니다.

<!-- However, if you wish, you may enable or disable specific rules in your `pint.json` file or use the `empty` preset and define the rules from scratch: -->
하지만 필요에 따라, 특정 룰만 개별적으로 활성화하거나 비활성화하고 싶다면, `pint.json` 파일에 직접 룰을 지정하거나, `empty` 프리셋을 사용해 처음부터 원하는 룰만 정의할 수 있습니다.

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

<!-- Pint is built on top of [PHP-CS-Fixer](https://github.com/FriendsOfPHP/PHP-CS-Fixer). Therefore, you may use any of its rules to fix code style issues in your project: [PHP-CS-Fixer Configurator](https://mlocati.github.io/php-cs-fixer-configurator). -->
Pint는 [PHP-CS-Fixer](https://github.com/FriendsOfPHP/PHP-CS-Fixer) 기반으로 만들어졌으므로, PHP-CS-Fixer가 제공하는 모든 룰을 사용할 수 있습니다. 자세한 룰 목록과 구성을 확인하려면 [PHP-CS-Fixer Configurator](https://mlocati.github.io/php-cs-fixer-configurator)를 참고하세요.

<a name="excluding-files-or-folders"></a>
<!-- ### Excluding Files / Folders -->
### Excluding Files / Folders

<!-- By default, Pint will inspect all `.php` files in your project except those in the `vendor` directory. If you wish to exclude more folders, you may do so using the `exclude` configuration option: -->
기본적으로 Pint는 `vendor` 디렉터리를 제외한 프로젝트 내 모든 `.php` 파일을 검사합니다. 그 외에 특정 폴더를 추가로 제외하고 싶을 때는 `exclude` 설정 옵션을 사용할 수 있습니다.

```json
{
    "exclude": [
        "my-specific/folder"
    ]
}
```

<!-- If you wish to exclude all files that contain a given name pattern, you may do so using the `notName` configuration option: -->
특정 이름 패턴을 가진 모든 파일을 제외하려면 `notName` 옵션을 사용할 수 있습니다.

```json
{
    "notName": [
        "*-my-file.php"
    ]
}
```

<!-- If you would like to exclude a file by providing an exact path to the file, you may do so using the `notPath` configuration option: -->
정확한 경로를 지정하여 특정 파일을 제외하고 싶을 때는 `notPath` 옵션을 사용합니다.

```json
{
    "notPath": [
        "path/to/excluded-file.php"
    ]
}
```

<a name="continuous-integration"></a>
<!-- ## Continuous Integration -->
## Continuous Integration

<a name="running-tests-on-github-actions"></a>
<!-- ### GitHub Actions -->
### GitHub Actions

<!-- To automate linting your project with Laravel Pint, you can configure [GitHub Actions](https://github.com/features/actions) to run Pint whenever new code is pushed to GitHub. First, be sure to grant "Read and write permissions" to workflows within GitHub at **Settings > Actions > General > Workflow permissions**. Then, create a `.github/workflows/lint.yml` file with the following content: -->
프로젝트에 Laravel Pint를 적용해 코드 린팅을 자동화하려면 [GitHub Actions](https://github.com/features/actions)를 이용해 코드를 푸시할 때마다 Pint를 실행하도록 설정할 수 있습니다. 먼저 **Settings > Actions > General > Workflow permissions**에서 워크플로에 "읽기 및 쓰기 권한(Read and write permissions)"을 부여해야 합니다. 그 후, 다음과 같이 `.github/workflows/lint.yml` 파일을 생성합니다.

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
        uses: actions/checkout@v4

      - name: Setup PHP
        uses: shivammathur/setup-php@v2
        with:
          php-version: ${{ matrix.php }}
          extensions: json, dom, curl, libxml, mbstring
          coverage: none

      - name: Install Pint
        run: composer global require laravel/pint

      - name: Run Pint
        run: pint

      - name: Commit linted files
        uses: stefanzweifel/git-auto-commit-action@v5
```
