<!-- # Localization -->
# Localization

- [Introduction](#introduction)
    - [Publishing the Language Files](#publishing-the-language-files)
    - [Configuring the Locale](#configuring-the-locale)
    - [Pluralization Language](#pluralization-language)
- [Defining Translation Strings](#defining-translation-strings)
    - [Using Short Keys](#using-short-keys)
    - [Using Translation Strings as Keys](#using-translation-strings-as-keys)
- [Retrieving Translation Strings](#retrieving-translation-strings)
    - [Replacing Parameters in Translation Strings](#replacing-parameters-in-translation-strings)
    - [Pluralization](#pluralization)
- [Overriding Package Language Files](#overriding-package-language-files)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

> [!NOTE]
> 기본적으로, Laravel 애플리케이션 골격에는 `lang` 디렉터리가 포함되어 있지 않습니다. Laravel의 언어 파일을 사용자화하려면 `lang:publish` Artisan 명령어로 해당 파일들을 배포할 수 있습니다.

<!-- Laravel's localization features provide a convenient way to retrieve strings in various languages, allowing you to easily support multiple languages within your application. -->
Laravel의 로컬라이제이션 기능은 다양한 언어의 문자열을 편리하게 가져올 수 있는 방법을 제공하여, 애플리케이션 내에서 다국어 지원을 쉽게 할 수 있게 합니다.

<!-- Laravel provides two ways to manage translation strings. First, language strings may be stored in files within the application's `lang` directory. Within this directory, there may be subdirectories for each language supported by the application. This is the approach Laravel uses to manage translation strings for built-in Laravel features such as validation error messages: -->
Laravel은 번역 문자열을 관리하는 두 가지 방식을 제공합니다. 첫 번째는 애플리케이션의 `lang` 디렉터리에 파일로 저장하는 방법입니다. 이 디렉터리 내에는 애플리케이션에서 지원하는 각 언어별 하위 디렉터리가 존재할 수 있습니다. 이 방식은 Laravel에서 내장 기능(예: 유효성 검증 오류 메시지)의 번역 문자열을 관리할 때 주로 사용합니다:

```text
/lang
    /en
        messages.php
    /es
        messages.php
```

<!-- Or, translation strings may be defined within JSON files that are placed within the `lang` directory. When taking this approach, each language supported by your application would have a corresponding JSON file within this directory. This approach is recommended for applications that have a large number of translatable strings: -->
또 다른 방식은 `lang` 디렉터리에 JSON 파일을 두고 번역 문자열을 정의하는 것입니다. 이 방법에서는 애플리케이션에서 지원하는 각 언어별로 대응하는 JSON 파일을 두게 됩니다. 번역 문자열이 많을 경우 이 방식을 권장합니다:

```text
/lang
    en.json
    es.json
```

<!-- We'll discuss each approach to managing translation strings within this documentation. -->
이 문서에서는 두 가지 번역 문자열 관리 방식을 차례로 설명합니다.

<a name="publishing-the-language-files"></a>
<!-- ### Publishing the Language Files -->
### Publishing the Language Files

<!-- By default, the Laravel application skeleton does not include the `lang` directory. If you would like to customize Laravel's language files or create your own, you should scaffold the `lang` directory via the `lang:publish` Artisan command. The `lang:publish` command will create the `lang` directory in your application and publish the default set of language files used by Laravel: -->
기본적으로 Laravel 애플리케이션 골격에는 `lang` 디렉터리가 포함되어 있지 않습니다. Laravel 언어 파일을 사용자화하거나 직접 생성하려면 `lang:publish` Artisan 명령어로 `lang` 디렉터리를 스캐폴딩하는 것이 좋습니다. `lang:publish` 명령어는 애플리케이션에 `lang` 디렉터리를 생성하고 Laravel에서 사용하는 기본 언어 파일 세트를 배포합니다:

```shell
php artisan lang:publish
```

<a name="configuring-the-locale"></a>
<!-- ### Configuring the Locale -->
### Configuring the Locale

<!-- The default language for your application is stored in the `config/app.php` configuration file's `locale` configuration option, which is typically set using the `APP_LOCALE` environment variable. You are free to modify this value to suit the needs of your application. -->
애플리케이션의 기본 언어는 보통 `config/app.php` 설정 파일 내 `locale` 옵션에 저장되며, 이는 일반적으로 `APP_LOCALE` 환경 변수를 통해 설정됩니다. 필요에 따라 이 값을 자유롭게 변경할 수 있습니다.

<!-- You may also configure a "fallback language", which will be used when the default language does not contain a given translation string. Like the default language, the fallback language is also configured in the `config/app.php` configuration file, and its value is typically set using the `APP_FALLBACK_LOCALE` environment variable. -->
또한, 기본 언어에 해당 번역이 없을 때 사용할 "대체 언어"도 설정할 수 있습니다. 대체 언어 역시 `config/app.php` 파일에서 설정되고, 보통 `APP_FALLBACK_LOCALE` 환경 변수로 값이 지정됩니다.

<!-- You may modify the default language for a single HTTP request at runtime using the `setLocale` method provided by the `App` facade: -->
실행 중 단일 HTTP 요청에 대해 기본 언어를 변경하려면 `App` 파사드에서 제공하는 `setLocale` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\App;

Route::get('/greeting/{locale}', function (string $locale) {
    if (! in_array($locale, ['en', 'es', 'fr'])) {
        abort(400);
    }

    App::setLocale($locale);

    // ...
});
```

<a name="determining-the-current-locale"></a>
<!-- #### Determining the Current Locale -->
#### Determining the Current Locale

<!-- You may use the `currentLocale` and `isLocale` methods on the `App` facade to determine the current locale or check if the locale is a given value: -->
현재 로케일을 확인하거나 특정 로케일인지 확인할 때는 `App` 파사드의 `currentLocale` 및 `isLocale` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\App;

$locale = App::currentLocale();

if (App::isLocale('en')) {
    // ...
}
```

<a name="pluralization-language"></a>
<!-- ### Pluralization Language -->
### Pluralization Language

<!-- <div class="code-list-no-flex-break"> -->
<div class="code-list-no-flex-break">

<!-- You may instruct Laravel's "pluralizer", which is used by Eloquent and other portions of the framework to convert singular strings to plural strings, to use a language other than English. This may be accomplished by invoking the `useLanguage` method within the `boot` method of one of your application's service providers. The pluralizer's currently supported languages are: `french`, `norwegian-bokmal`, `portuguese`, `spanish`, and `turkish`: -->
Eloquent와 프레임워크 일부에서 단수형 문자열을 복수형으로 변환하는 데 사용하는 Laravel의 "pluralizer"에 영어 외 다른 언어를 사용하도록 지시할 수 있습니다. 이 작업은 애플리케이션의 서비스 프로바이더 중 하나의 `boot` 메서드 내에서 `useLanguage` 메서드를 호출하면 됩니다. 현재 pluralizer가 지원하는 언어는 `french`(프랑스어), `norwegian-bokmal`(노르웨이어), `portuguese`(포르투갈어), `spanish`(스페인어), `turkish`(터키어)입니다.

<!-- </div> -->
</div>

```php
use Illuminate\Support\Pluralizer;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Pluralizer::useLanguage('spanish');

    // ...
}
```

> [!WARNING]
> pluralizer의 언어를 변경하는 경우, 반드시 Eloquent 모델의 [table names](/docs/13.x/eloquent#table-names)을 명시적으로 정의해야 합니다.

<a name="defining-translation-strings"></a>
<!-- ## Defining Translation Strings -->
## Defining Translation Strings

<a name="using-short-keys"></a>
<!-- ### Using Short Keys -->
### Using Short Keys

<!-- Typically, translation strings are stored in files within the `lang` directory. Within this directory, there should be a subdirectory for each language supported by your application. This is the approach Laravel uses to manage translation strings for built-in Laravel features such as validation error messages: -->
일반적으로 번역 문자열은 `lang` 디렉터리 내 파일에 저장합니다. 이 디렉터리 내부에는 애플리케이션에서 지원하는 각 언어별 하위 디렉터리가 있어야 합니다. 이 방식은 Laravel의 내장 기능(예: 유효성 검증 메시지) 번역 문자열 관리에 사용됩니다:

```text
/lang
    /en
        messages.php
    /es
        messages.php
```

<!-- All language files return an array of keyed strings. For example: -->
모든 언어 파일은 키-값 형태의 배열을 반환합니다. 예시:

```php
<?php

// lang/en/messages.php

return [
    'welcome' => 'Welcome to our application!',
];
```

> [!WARNING]
> 지명이나 국가는 ISO 15897 표준에 따라 언어 디렉터리를 명명해야 합니다. 예를 들어 영국 영어는 "en_GB"로, "en-gb"가 아닙니다.

<a name="using-translation-strings-as-keys"></a>
<!-- ### Using Translation Strings as Keys -->
### Using Translation Strings as Keys

<!-- For applications with a large number of translatable strings, defining every string with a "short key" can become confusing when referencing the keys in your views and it is cumbersome to continually invent keys for every translation string supported by your application. -->
번역 가능한 문자열이 많은 애플리케이션에서는 모든 문자열을 "짧은 키"로 정의하면 뷰에서 키를 참조할 때 혼란스러워질 수 있고, 지원하는 모든 번역 문자열마다 키를 계속 새로 만들어 내는 것도 번거롭습니다.

<!-- For this reason, Laravel also provides support for defining translation strings using the "default" translation of the string as the key. Language files that use translation strings as keys are stored as JSON files in the `lang` directory. For example, if your application has a Spanish translation, you should create a `lang/es.json` file: -->
이러한 이유로 Laravel은 문자열의 "기본" 번역 자체를 키로 사용해 번역 문자열을 정의하는 방식도 지원합니다. 번역 문자열을 키로 사용하는 언어 파일은 `lang` 디렉터리에 JSON 파일로 저장합니다. 예를 들어 애플리케이션이 스페인어 번역을 지원한다면 `lang/es.json` 파일을 만들어야 합니다:

```json
{
    "I love programming.": "Me encanta programar."
}
```

<!-- #### Key / File Conflicts -->
#### Key / File Conflicts

<!-- You should not define translation string keys that conflict with other translation filenames. For example, translating `__('Action')` for the "NL" locale while a `nl/action.php` file exists but a `nl.json` file does not exist will result in the translator returning the entire contents of `nl/action.php`. -->
다른 번역 파일명과 충돌하는 키를 정의해서는 안 됩니다. 예를 들어 `__('Action')`을 "NL" 로케일에서 번역하려 할 때 `nl/action.php` 파일이 존재하고 `nl.json` 파일은 없으면, 해당 번역자는 `nl/action.php` 파일 전체를 반환하게 됩니다.

<a name="retrieving-translation-strings"></a>
<!-- ## Retrieving Translation Strings -->
## Retrieving Translation Strings

<!-- You may retrieve translation strings from your language files using the `__` helper function. If you are using "short keys" to define your translation strings, you should pass the file that contains the key and the key itself to the `__` function using "dot" syntax. For example, let's retrieve the `welcome` translation string from the `lang/en/messages.php` language file: -->
`__` 헬퍼 함수를 이용해 언어 파일에서 번역 문자열을 가져올 수 있습니다. 짧은 키 방식을 사용할 경우, 키가 포함된 파일과 키 자체를 "dot"(닷) 구문으로 `__` 함수에 전달합니다. 예를 들어 `lang/en/messages.php` 파일 내 `welcome` 키 값을 가져올 때:

```php
echo __('messages.welcome');
```

<!-- If the specified translation string does not exist, the `__` function will return the translation string key. So, using the example above, the `__` function would return `messages.welcome` if the translation string does not exist. -->
만약 지정한 번역 문자열이 없으면 `__` 함수는 번역 문자열 키를 반환합니다. 따라서 위 예시에서 해당 번역 문자열이 없으면 `__` 함수는 `messages.welcome`을 반환합니다.

<!-- If you are using your [default translation strings as your translation keys](#using-translation-strings-as-keys), you should pass the default translation of your string to the `__` function; -->
[default translation strings as your translation keys](#using-translation-strings-as-keys)을 쓸 경우에는 `__` 함수에 해당 문자열의 기본 번역문을 그대로 넘깁니다:

```php
echo __('I love programming.');
```

<!-- Again, if the translation string does not exist, the `__` function will return the translation string key that it was given. -->
이 경우에도 번역 문자열이 없으면 `__` 함수는 전달받은 번역 문자열 키를 그대로 반환합니다.

<!-- If you are using the [Blade templating engine](/docs/13.x/blade), you may use the `{{ }}` echo syntax to display the translation string: -->
[Blade templating engine](/docs/13.x/blade)을 사용하는 경우, `{{ }}` 출력 구문을 활용할 수 있습니다:

```blade
{{ __('messages.welcome') }}
```

<a name="replacing-parameters-in-translation-strings"></a>
<!-- ### Replacing Parameters in Translation Strings -->
### Replacing Parameters in Translation Strings

<!-- If you wish, you may define placeholders in your translation strings. All placeholders are prefixed with a `:`. For example, you may define a welcome message with a placeholder name: -->
필요한 경우 번역 문자열 내에 플레이스홀더(자리표시자)를 정의할 수 있습니다. 모든 플레이스홀더는 `:`로 시작합니다. 예를 들어 이름을 넣는 환영 메시지를 정의할 수 있습니다:

```php
'welcome' => 'Welcome, :name',
```

<!-- To replace the placeholders when retrieving a translation string, you may pass an array of replacements as the second argument to the `__` function: -->
번역 문자열을 가져올 때 치환할 값은 `__` 함수의 두 번째 인자로 배열 형태로 전달합니다:

```php
echo __('messages.welcome', ['name' => 'dayle']);
```

<!-- If your placeholder contains all capital letters, or only has its first letter capitalized, the translated value will be capitalized accordingly: -->
플레이스홀더가 전부 대문자거나 첫 글자만 대문자일 경우, 치환된 값도 대응되는 형식으로 자동 변환됩니다:

```php
'welcome' => 'Welcome, :NAME', // Welcome, DAYLE
'goodbye' => 'Goodbye, :Name', // Goodbye, Dayle
```

<a name="object-replacement-formatting"></a>
<!-- #### Object Replacement Formatting -->
#### Object Replacement Formatting

<!-- If you attempt to provide an object as a translation placeholder, the object's `__toString` method will be invoked. The [__toString](https://www.php.net/manual/en/language.oop5.magic.php#object.tostring) method is one of PHP's built-in "magic methods". However, sometimes you may not have control over the `__toString` method of a given class, such as when the class that you are interacting with belongs to a third-party library. -->
번역 문자열 플레이스홀더에 객체를 사용할 경우, 해당 객체의 `__toString` 메서드가 호출됩니다. [__toString](https://www.php.net/manual/en/language.oop5.magic.php#object.tostring) 메서드는 PHP의 내장 "매직 메서드" 중 하나입니다. 그러나 간혹 서드파티 라이브러리 클래스 등, `__toString` 메서드를 직접 제어하기 어려운 경우도 있습니다.

<!-- In these cases, Laravel allows you to register a custom formatting handler for that particular type of object. To accomplish this, you should invoke the translator's `stringable` method. The `stringable` method accepts a closure, which should type-hint the type of object that it is responsible for formatting. Typically, the `stringable` method should be invoked within the `boot` method of your application's `AppServiceProvider` class: -->
이때 Laravel에서는 특정 객체 유형에 대해 커스텀 포맷팅 핸들러를 등록할 수 있습니다. 이를 위해 번역자(translator)의 `stringable` 메서드를 호출하면 됩니다. `stringable` 메서드는 클로저를 받으며, 이 클로저는 포맷팅을 책임질 객체 타입을 타입힌트로 명시해야 합니다. 보통 `stringable` 메서드는 애플리케이션 `AppServiceProvider` 클래스의 `boot` 메서드 내에서 호출합니다:

```php
use Illuminate\Support\Facades\Lang;
use Money\Money;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Lang::stringable(function (Money $money) {
        return $money->formatTo('en_GB');
    });
}
```

<a name="pluralization"></a>
<!-- ### Pluralization -->
### Pluralization

<!-- Pluralization is a complex problem, as different languages have a variety of complex rules for pluralization; however, Laravel can help you translate strings differently based on pluralization rules that you define. Using a `|` character, you may distinguish singular and plural forms of a string: -->
복수형 처리는 언어마다 다양한 복잡한 규칙이 있으므로 까다로운 문제이지만, Laravel은 사용자가 정의한 복수형 규칙에 따라 다르게 번역할 수 있게 도와줍니다. `|` 문자로 단수형과 복수형 구분이 가능합니다:

```php
'apples' => 'There is one apple|There are many apples',
```

<!-- Of course, pluralization is also supported when using [translation strings as keys](#using-translation-strings-as-keys): -->
물론 [translation strings as keys](#using-translation-strings-as-keys)에서도 복수형을 지원합니다:

```json
{
    "There is one apple|There are many apples": "Hay una manzana|Hay muchas manzanas"
}
```

<!-- You may even create more complex pluralization rules which specify translation strings for multiple ranges of values: -->
더욱 복잡한 복수형 규칙도 만들 수 있습니다. 예를 들어, 여러 개수 구간별 메시지를 지정할 수 있습니다:

```php
'apples' => '{0} There are none|[1,19] There are some|[20,*] There are many',
```

<!-- After defining a translation string that has pluralization options, you may use the `trans_choice` function to retrieve the line for a given "count". In this example, since the count is greater than one, the plural form of the translation string is returned: -->
복수형 옵션이 포함된 번역 문자열을 정의한 뒤에는 `trans_choice` 함수를 사용해 주어진 "개수"에 맞는 문장 형태를 가져옵니다. 아래 예에서는 1보다 크므로 복수형 번역 문자열이 반환됩니다:

```php
echo trans_choice('messages.apples', 10);
```

<!-- You may also define placeholder attributes in pluralization strings. These placeholders may be replaced by passing an array as the third argument to the `trans_choice` function: -->
복수형 문자열 안에 플레이스홀더도 정의할 수 있으며, 이는 `trans_choice` 함수의 세 번째 인자로 배열로 전달해 치환할 수 있습니다:

```php
'minutes_ago' => '{1} :value minute ago|[2,*] :value minutes ago',

echo trans_choice('time.minutes_ago', 5, ['value' => 5]);
```

<!-- If you would like to display the integer value that was passed to the `trans_choice` function, you may use the built-in `:count` placeholder: -->
`trans_choice` 함수에 전달한 정수 값을 표시하고 싶을 때는 내장 플레이스홀더인 `:count`를 사용할 수 있습니다:

```php
'apples' => '{0} There are none|{1} There is one|[2,*] There are :count',
```

<a name="overriding-package-language-files"></a>
<!-- ## Overriding Package Language Files -->
## Overriding Package Language Files

<!-- Some packages may ship with their own language files. Instead of changing the package's core files to tweak these lines, you may override them by placing files in the `lang/vendor/{package}/{locale}` directory. -->
일부 패키지는 자체 언어 파일을 포함하여 배포합니다. 패키지 코어 파일을 직접 수정하는 대신, `lang/vendor/{package}/{locale}` 디렉터리에 파일을 두어 번역 문자열을 덮어쓸 수 있습니다.

<!-- So, for example, if you need to override the English translation strings in `messages.php` for a package named `skyrim/hearthfire`, you should place a language file at: `lang/vendor/hearthfire/en/messages.php`. Within this file, you should only define the translation strings you wish to override. Any translation strings you don't override will still be loaded from the package's original language files. -->
예를 들어 `skyrim/hearthfire`라는 패키지의 영어 `messages.php` 번역 문자열을 덮어쓰려면, `lang/vendor/hearthfire/en/messages.php` 경로에 파일을 두면 됩니다. 이 파일에는 덮어쓸 번역 문자열만 정의하면 되며, 수정하지 않은 문자열은 원래 패키지 언어 파일에서 계속 로드됩니다.
