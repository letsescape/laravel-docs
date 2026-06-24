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

<!-- [Laravel Pint](https://github.com/laravel/pint) is an opinionated PHP code style fixer for minimalists. Pint is built on top of [PHP CS Fixer](https://github.com/FriendsOfPHP/PHP-CS-Fixer) and makes it simple to ensure that your code style stays clean and consistent. -->
[Laravel Pint](https://github.com/laravel/pint)는 간결함을 선호하는 개발자를 위한 의견이 반영된 PHP 코드 스타일 수정 도구입니다. Pint는 [PHP CS Fixer](https://github.com/FriendsOfPHP/PHP-CS-Fixer)를 기반으로 만들어졌으며, 코드 스타일을 깔끔하고 일관되게 유지하기 쉽게 해줍니다.

<!-- Pint is automatically installed with all new Laravel applications so you may start using it immediately. By default, Pint does not require any configuration and will fix code style issues in your code by following the opinionated coding style of Laravel. -->
Pint는 새 Laravel 애플리케이션에 자동으로 설치되므로 바로 사용할 수 있습니다. 기본적으로 Pint는 별도의 설정이 필요하지 않으며, Laravel의 의견이 반영된 코딩 스타일을 따라 코드의 스타일 문제를 수정합니다.

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- Pint is included in recent releases of the Laravel framework, so installation is typically unnecessary. However, for older applications, you may install Laravel Pint via Composer: -->
Pint는 최근 Laravel 프레임워크 릴리스에 포함되어 있으므로 일반적으로 별도 설치가 필요하지 않습니다. 하지만 오래된 애플리케이션에서는 Composer를 통해 Laravel Pint를 설치할 수 있습니다.

```shell
composer require laravel/pint --dev
```

<a name="running-pint"></a>
<!-- ## Running Pint -->
## Running Pint

<!-- You can instruct Pint to fix code style issues by invoking the `pint` binary that is available in your project's `vendor/bin` directory: -->
프로젝트의 `vendor/bin` 디렉터리에 있는 `pint` 바이너리를 실행하여 Pint가 코드 스타일 문제를 수정하도록 할 수 있습니다.

```shell
./vendor/bin/pint
```

<!-- If you would like Pint to run in parallel mode (experimental) for improved performance, you may use the `--parallel` option: -->
성능 향상을 위해 Pint를 병렬 모드(실험적 기능)로 실행하려면 `--parallel` 옵션을 사용할 수 있습니다.

```shell
./vendor/bin/pint --parallel
```

<!-- Parallel mode also allows you to specify the maximum number of processes to run via the `--max-processes` option. If this option is not provided, Pint will use every available core on your machine: -->
병렬 모드에서는 `--max-processes` 옵션으로 실행할 최대 프로세스 수를 지정할 수도 있습니다. 이 옵션을 제공하지 않으면 Pint는 사용 중인 머신에서 사용 가능한 모든 코어를 사용합니다.

```shell
./vendor/bin/pint --parallel --max-processes=4
```

<!-- You may also run Pint on specific files or directories: -->
특정 파일이나 디렉터리에 대해서만 Pint를 실행할 수도 있습니다.

```shell
./vendor/bin/pint app/Models

./vendor/bin/pint app/Models/User.php
```

<!-- Pint will display a thorough list of all of the files that it updates. You can view even more detail about Pint's changes by providing the `-v` option when invoking Pint: -->
Pint는 업데이트한 모든 파일의 상세 목록을 표시합니다. Pint가 변경한 내용을 더 자세히 보려면 Pint를 실행할 때 `-v` 옵션을 제공하면 됩니다.

```shell
./vendor/bin/pint -v
```

<!-- If you would like Pint to simply inspect your code for style errors without actually changing the files, you may use the `--test` option. Pint will return a non-zero exit code if any code style errors are found: -->
파일을 실제로 변경하지 않고 코드에 스타일 오류가 있는지만 검사하려면 `--test` 옵션을 사용할 수 있습니다. 코드 스타일 오류가 발견되면 Pint는 0이 아닌 종료 코드를 반환합니다.

```shell
./vendor/bin/pint --test
```

<!-- If you would like Pint to only modify the files that differ from the provided branch according to Git, you may use the `--diff=[branch]` option. This can be effectively used in your CI environment (like GitHub actions) to save time by only inspecting new or modified files: -->
Git 기준으로 제공한 브랜치와 다른 파일만 Pint가 수정하도록 하려면 `--diff=[branch]` 옵션을 사용할 수 있습니다. 이 옵션은 GitHub Actions 같은 CI 환경에서 새 파일이나 수정된 파일만 검사하여 시간을 절약하는 데 효과적으로 사용할 수 있습니다.

```shell
./vendor/bin/pint --diff=main
```

<!-- If you would like Pint to only modify the files that have uncommitted changes according to Git, you may use the `--dirty` option: -->
Git 기준으로 커밋되지 않은 변경 사항이 있는 파일만 Pint가 수정하도록 하려면 `--dirty` 옵션을 사용할 수 있습니다.

```shell
./vendor/bin/pint --dirty
```

<!-- If you would like Pint to fix any files with code style errors but also exit with a non-zero exit code if any errors were fixed, you may use the `--repair` option: -->
코드 스타일 오류가 있는 파일을 수정하되, 오류가 수정된 경우 0이 아닌 종료 코드로 종료되도록 하려면 `--repair` 옵션을 사용할 수 있습니다.

```shell
./vendor/bin/pint --repair
```

<a name="configuring-pint"></a>
<!-- ## Configuring Pint -->
## Configuring Pint

<!-- As previously mentioned, Pint does not require any configuration. However, if you wish to customize the presets, rules, or inspected folders, you may do so by creating a `pint.json` file in your project's root directory: -->
앞서 언급했듯이 Pint는 별도의 설정이 필요하지 않습니다. 하지만 프리셋, 규칙 또는 검사할 폴더를 사용자 정의하려면 프로젝트 루트 디렉터리에 `pint.json` 파일을 만들면 됩니다.

```json
{
    "preset": "laravel"
}
```

<!-- In addition, if you wish to use a `pint.json` from a specific directory, you may provide the `--config` option when invoking Pint: -->
또한 특정 디렉터리에 있는 `pint.json`을 사용하려면 Pint를 실행할 때 `--config` 옵션을 제공할 수 있습니다.

```shell
./vendor/bin/pint --config vendor/my-company/coding-style/pint.json
```

<a name="presets"></a>
<!-- ### Presets -->
### Presets

<!-- Presets define a set of rules that can be used to fix code style issues in your code. By default, Pint uses the `laravel` preset, which fixes issues by following the opinionated coding style of Laravel. However, you may specify a different preset by providing the `--preset` option to Pint: -->
프리셋은 코드의 스타일 문제를 수정하는 데 사용할 수 있는 규칙 집합을 정의합니다. 기본적으로 Pint는 Laravel의 의견이 반영된 코딩 스타일을 따라 문제를 수정하는 `laravel` 프리셋을 사용합니다. 하지만 Pint에 `--preset` 옵션을 제공하여 다른 프리셋을 지정할 수 있습니다.

```shell
./vendor/bin/pint --preset psr12
```

<!-- If you wish, you may also set the preset in your project's `pint.json` file: -->
원한다면 프로젝트의 `pint.json` 파일에서 프리셋을 설정할 수도 있습니다.

```json
{
    "preset": "psr12"
}
```

<!-- Pint's currently supported presets are: `laravel`, `per`, `psr12`, `symfony`, and `empty`. -->
현재 Pint가 지원하는 프리셋은 `laravel`, `per`, `psr12`, `symfony`, `empty`입니다.

<a name="rules"></a>
<!-- ### Rules -->
### Rules

<!-- Rules are style guidelines that Pint will use to fix code style issues in your code. As mentioned above, presets are predefined groups of rules that should be perfect for most PHP projects, so you typically will not need to worry about the individual rules they contain. -->
규칙은 Pint가 코드의 스타일 문제를 수정할 때 사용하는 스타일 지침입니다. 위에서 언급했듯이 프리셋은 대부분의 PHP 프로젝트에 적합하도록 미리 정의된 규칙 그룹이므로, 일반적으로 프리셋에 포함된 개별 규칙을 신경 쓸 필요는 없습니다.

<!-- However, if you wish, you may enable or disable specific rules in your `pint.json` file or use the `empty` preset and define the rules from scratch: -->
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

<!-- Pint is built on top of [PHP CS Fixer](https://github.com/FriendsOfPHP/PHP-CS-Fixer). Therefore, you may use any of its rules to fix code style issues in your project: [PHP CS Fixer Configurator](https://mlocati.github.io/php-cs-fixer-configurator). -->
Pint는 [PHP CS Fixer](https://github.com/FriendsOfPHP/PHP-CS-Fixer)를 기반으로 만들어졌습니다. 따라서 프로젝트의 코드 스타일 문제를 수정하기 위해 PHP CS Fixer의 모든 규칙을 사용할 수 있습니다. [PHP CS Fixer Configurator](https://mlocati.github.io/php-cs-fixer-configurator)를 참고하십시오.

<a name="excluding-files-or-folders"></a>
<!-- ### Excluding Files / Folders -->
### Excluding Files / Folders

<!-- By default, Pint will inspect all `.php` files in your project except those in the `vendor` directory. If you wish to exclude more folders, you may do so using the `exclude` configuration option: -->
기본적으로 Pint는 `vendor` 디렉터리에 있는 파일을 제외하고 프로젝트의 모든 `.php` 파일을 검사합니다. 더 많은 폴더를 제외하려면 `exclude` 설정 옵션을 사용할 수 있습니다.

```json
{
    "exclude": [
        "my-specific/folder"
    ]
}
```

<!-- If you wish to exclude all files that contain a given name pattern, you may do so using the `notName` configuration option: -->
특정 이름 패턴을 포함하는 모든 파일을 제외하려면 `notName` 설정 옵션을 사용할 수 있습니다.

```json
{
    "notName": [
        "*-my-file.php"
    ]
}
```

<!-- If you would like to exclude a file by providing an exact path to the file, you may do so using the `notPath` configuration option: -->
파일의 정확한 경로를 제공하여 특정 파일을 제외하려면 `notPath` 설정 옵션을 사용할 수 있습니다.

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
