<!-- # Laravel Pint -->
# Laravel Pint

- [Introduction](#introduction)
- [Installation](#installation)
- [Running Pint](#running-pint)
- [Configuring Pint](#configuring-pint)
    - [Presets](#presets)
    - [Rules](#rules)
    - [Excluding Files / Folders](#excluding-files-or-folders)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- [Laravel Pint](https://github.com/laravel/pint) is an opinionated PHP code style fixer for minimalists. Pint is built on top of PHP-CS-Fixer and makes it simple to ensure that your code style stays clean and consistent. -->
[Laravel Pint](https://github.com/laravel/pint)는 미니멀리스트를 위한, 의견이 반영된(opinionated) PHP 코드 스타일 자동 교정 도구입니다. Pint는 PHP-CS-Fixer를 기반으로 만들어졌으며, 여러분의 코드 스타일을 깔끔하고 일관되게 유지할 수 있도록 단순한 사용법을 제공합니다.

<!-- Pint is automatically installed with all new Laravel applications so you may start using it immediately. By default, Pint does not require any configuration and will fix code style issues in your code by following the opinionated coding style of Laravel. -->
Pint는 모든 새로운 Laravel 애플리케이션에 자동으로 설치되기 때문에, 별도 설치 없이 바로 사용할 수 있습니다. 기본적으로 Pint는 별도의 설정 없이도 Laravel의 권장 코딩 스타일을 따라 여러분의 코드 스타일 문제를 자동으로 고쳐줍니다.

<a name="installation"></a>
<!-- ## Installation -->
## Installation

<!-- Pint is included in recent releases of the Laravel framework, so installation is typically unnecessary. However, for older applications, you may install Laravel Pint via Composer: -->
Pint는 최신 버전의 Laravel 프레임워크에 기본 포함되어 있으므로, 별도의 설치가 필요하지 않습니다. 하지만 예전 버전의 애플리케이션에서는 Composer를 통해 Laravel Pint를 설치할 수 있습니다:

```shell
composer require laravel/pint --dev
```

<a name="running-pint"></a>
<!-- ## Running Pint -->
## Running Pint

<!-- You can instruct Pint to fix code style issues by invoking the `pint` binary that is available in your project's `vendor/bin` directory: -->
Pint로 코드 스타일 문제를 자동으로 교정하려면, 여러분 프로젝트의 `vendor/bin` 디렉터리에 있는 `pint` 바이너리를 실행하면 됩니다:

```shell
./vendor/bin/pint
```

<!-- You may also run Pint on specific files or directories: -->
Pint를 특정 파일이나 디렉터리에만 실행할 수도 있습니다:

```shell
./vendor/bin/pint app/Models

./vendor/bin/pint app/Models/User.php
```

<!-- Pint will display a thorough list of all of the files that it updates. You can view even more detail about Pint's changes by providing the `-v` option when invoking Pint: -->
Pint는 업데이트한 모든 파일의 목록을 자세하게 보여줍니다. Pint가 적용한 변경 내역을 더 자세히 확인하고 싶다면, Pint 실행 시 `-v` 옵션을 추가하면 됩니다:

```shell
./vendor/bin/pint -v
```

<!-- If you would like Pint to simply inspect your code for style errors without actually changing the files, you may use the `--test` option: -->
코드를 실제로 수정하지 않고 스타일 오류만 검사하고 싶다면, `--test` 옵션을 사용하세요:

```shell
./vendor/bin/pint --test
```

<!-- If you would like Pint to only modify the files that have uncommitted changes according to Git, you may use the `--dirty` option: -->
Git에서 커밋되지 않은 변경 사항이 있는 파일에만 Pint를 적용하고 싶다면, `--dirty` 옵션을 사용할 수 있습니다:

```shell
./vendor/bin/pint --dirty
```

<a name="configuring-pint"></a>
<!-- ## Configuring Pint -->
## Configuring Pint

<!-- As previously mentioned, Pint does not require any configuration. However, if you wish to customize the presets, rules, or inspected folders, you may do so by creating a `pint.json` file in your project's root directory: -->
앞서 설명한 것처럼, Pint는 기본적으로 아무런 설정 없이도 사용할 수 있습니다. 하지만 프리셋, 규칙, 검사 대상 폴더 등을 원하는 대로 커스터마이즈하고 싶다면, 프로젝트 루트 디렉터리에 `pint.json` 파일을 만들면 됩니다:

```json
{
    "preset": "laravel"
}
```

<!-- In addition, if you wish to use a `pint.json` from a specific directory, you may provide the `--config` option when invoking Pint: -->
또한, 특정 디렉터리에 있는 `pint.json` 파일을 사용하고 싶다면, Pint 실행 시 `--config` 옵션을 지정할 수 있습니다:

```shell
pint --config vendor/my-company/coding-style/pint.json
```

<a name="presets"></a>
<!-- ### Presets -->
### Presets

<!-- Presets defines a set of rules that can be used to fix code style issues in your code. By default, Pint uses the `laravel` preset, which fixes issues by following the opinionated coding style of Laravel. However, you may specify a different preset by providing the `--preset` option to Pint: -->
프리셋은 코드 스타일 문제를 고치는 데 사용할 규칙 세트입니다. 기본적으로 Pint는 `laravel` 프리셋을 사용하여, Laravel의 권장 코딩 스타일 기준에 맞춰 문제를 해결합니다. 하지만, 원한다면 Pint를 실행할 때 `--preset` 옵션을 주어 다른 프리셋을 지정할 수 있습니다:

```shell
pint --preset psr12
```

<!-- If you wish, you may also set the preset in your project's `pint.json` file: -->
원하면, 프로젝트의 `pint.json` 파일에 프리셋을 미리 지정해 둘 수도 있습니다:

```json
{
    "preset": "psr12"
}
```

<!-- Pint's currently supported presets are: `laravel`, `psr12`, and `symfony`. -->
현재 Pint가 지원하는 프리셋은 다음과 같습니다: `laravel`, `psr12`, `symfony`.

<a name="rules"></a>
<!-- ### Rules -->
### Rules

<!-- Rules are style guidelines that Pint will use to fix code style issues in your code. As mentioned above, presets are predefined groups of rules that should be perfect for most PHP projects, so you typically will not need to worry about the individual rules they contain. -->
규칙은 Pint가 코드 스타일을 수정할 때 참고하는 스타일 가이드라인을 의미합니다. 위에서 설명한 것처럼, 프리셋은 여러 개의 규칙이 미리 묶여 있는 형태이므로, 일반적으로는 프리셋만 신경 써도 충분합니다.

<!-- However, if you wish, you may enable or disable specific rules in your `pint.json` file: -->
하지만 원한다면, `pint.json` 파일에서 개별 규칙을 직접 활성화하거나 비활성화할 수도 있습니다:

```json
{
    "preset": "laravel",
    "rules": {
        "simplified_null_return": true,
        "braces": false,
        "new_with_braces": {
            "anonymous_class": false,
            "named_class": false
        }
    }
}
```

<!-- Pint is built on top of [PHP-CS-Fixer](https://github.com/FriendsOfPHP/PHP-CS-Fixer). Therefore, you may use any of its rules to fix code style issues in your project: [PHP-CS-Fixer Configurator](https://mlocati.github.io/php-cs-fixer-configurator). -->
Pint는 [PHP-CS-Fixer](https://github.com/FriendsOfPHP/PHP-CS-Fixer)를 기반으로 동작합니다. 따라서, 해당 도구에서 제공하는 모든 규칙을 활용해 프로젝트의 코드 스타일 문제를 교정할 수 있습니다: [PHP-CS-Fixer Configurator](https://mlocati.github.io/php-cs-fixer-configurator).

<a name="excluding-files-or-folders"></a>
<!-- ### Excluding Files / Folders -->
### Excluding Files / Folders

<!-- By default, Pint will inspect all `.php` files in your project except those in the `vendor` directory. If you wish to exclude more folders, you may do so using the `exclude` configuration option: -->
기본적으로 Pint는 프로젝트 내의 모든 `.php` 파일을 검사하지만, `vendor` 디렉터리는 자동으로 제외됩니다. 추가로 제외할 폴더가 있다면, `exclude` 설정 옵션을 사용하여 지정할 수 있습니다:

```json
{
    "exclude": [
        "my-specific/folder"
    ]
}
```

<!-- If you wish to exclude all files that contain a given name pattern, you may do so using the `notName` configuration option: -->
특정 이름 패턴이 포함된 모든 파일을 제외하고 싶다면, `notName` 옵션을 사용할 수 있습니다:

```json
{
    "notName": [
        "*-my-file.php"
    ]
}
```

<!-- If you would like to exclude a file by providing an exact path to the file, you may do so using the `notPath` configuration option: -->
정확한 경로로 특정 파일을 제외하고 싶다면, `notPath` 옵션을 사용하세요:

```json
{
    "notPath": [
        "path/to/excluded-file.php"
    ]
}
```