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
> 기본적으로 Laravel 애플리케이션 스캐폴딩에는 `lang` 디렉터리가 포함되어 있지 않습니다. Laravel의 언어 파일을 커스터마이즈하고 싶다면 `lang:publish` Artisan 명령어를 통해 언어 파일을 배포할 수 있습니다.

<!-- Laravel's localization features provide a convenient way to retrieve strings in various languages, allowing you to easily support multiple languages within your application. -->
Laravel의 로컬라이제이션(localization, 다국어 지원) 기능을 사용하면, 다양한 언어의 문자열을 쉽게 가져올 수 있습니다. 이를 통해 하나의 애플리케이션에서 여러 언어를 편리하게 지원할 수 있습니다.

<!-- Laravel provides two ways to manage translation strings. First, language strings may be stored in files within the application's `lang` directory. Within this directory, there may be subdirectories for each language supported by the application. This is the approach Laravel uses to manage translation strings for built-in Laravel features such as validation error messages: -->
Laravel은 번역 문자열을 관리하는 두 가지 방법을 제공합니다. 첫 번째 방법은 애플리케이션의 `lang` 디렉터리 내에 언어 파일을 저장하는 것입니다. 이 디렉터리 안에는 애플리케이션에서 지원하는 언어별로 각각의 하위 디렉터리가 존재할 수 있습니다. 이 방식은 유효성 검증 에러 메시지 등 Laravel의 기본 기능에서 사용하는 번역 문자열을 저장할 때 사용됩니다.


```
/lang
    /en
        messages.php
    /es
        messages.php
```


<!-- Or, translation strings may be defined within JSON files that are placed within the `lang` directory. When taking this approach, each language supported by your application would have a corresponding JSON file within this directory. This approach is recommended for applications that have a large number of translatable strings: -->
두 번째 방법은 번역 문자열을 JSON 파일로 정의하고 이 파일들을 `lang` 디렉터리에 두는 것입니다. 이 방법을 사용할 경우, 지원하는 각 언어마다 해당 언어의 JSON 파일을 디렉터리 내에 하나씩 만들어야 합니다. 번역할 문자열의 양이 많은 애플리케이션에는 이 방식을 추천합니다.

```
/lang
    en.json
    es.json
```

<!-- We'll discuss each approach to managing translation strings within this documentation. -->
이 문서에서는 각각의 번역 문자열 관리 방식에 대해 자세히 설명합니다.

<a name="publishing-the-language-files"></a>
<!-- ### Publishing the Language Files -->
### Publishing the Language Files

<!-- By default, the Laravel application skeleton does not include the `lang` directory. If you would like to customize Laravel's language files or create your own, you should scaffold the `lang` directory via the `lang:publish` Artisan command. The `lang:publish` command will create the `lang` directory in your application and publish the default set of language files used by Laravel: -->
기본적으로 Laravel 애플리케이션 스캐폴딩에는 `lang` 디렉터리가 포함되어 있지 않습니다. 만약 Laravel의 언어 파일을 커스터마이즈하거나 직접 만들고 싶다면, `lang:publish` Artisan 명령어로 `lang` 디렉터리를 스캐폴딩해야 합니다. `lang:publish` 명령어는 애플리케이션에 `lang` 디렉터리를 생성하고 Laravel에서 사용하는 기본 언어 파일들을 배포합니다.

```shell
php artisan lang:publish
```

<a name="configuring-the-locale"></a>
<!-- ### Configuring the Locale -->
### Configuring the Locale

<!-- The default language for your application is stored in the `config/app.php` configuration file's `locale` configuration option. You are free to modify this value to suit the needs of your application. -->
애플리케이션의 기본 언어(로케일)는 `config/app.php` 설정 파일의 `locale` 옵션에 저장되어 있습니다. 여러분의 애플리케이션에 맞게 이 값을 자유롭게 수정하실 수 있습니다.

<!-- You may modify the default language for a single HTTP request at runtime using the `setLocale` method provided by the `App` facade: -->
실행 중에 한 번의 HTTP 요청에 대해 기본 언어를 변경하고 싶다면, `App` 파사드에서 제공하는 `setLocale` 메서드를 사용할 수 있습니다.

```
use Illuminate\Support\Facades\App;

Route::get('/greeting/{locale}', function (string $locale) {
    if (! in_array($locale, ['en', 'es', 'fr'])) {
        abort(400);
    }

    App::setLocale($locale);

    // ...
});
```

<!-- You may configure a "fallback language", which will be used when the active language does not contain a given translation string. Like the default language, the fallback language is also configured in the `config/app.php` configuration file: -->
"폴백 언어(fallback language)"도 설정할 수 있습니다. 폴백 언어란 현재 사용 중인 언어 파일에 특정 번역 문자열이 없을 때 대신 사용할 언어를 의미합니다. 폴백 언어 역시 `config/app.php` 파일에서 설정합니다.

```
'fallback_locale' => 'en',
```

<a name="determining-the-current-locale"></a>
<!-- #### Determining the Current Locale -->
#### Determining the Current Locale

<!-- You may use the `currentLocale` and `isLocale` methods on the `App` facade to determine the current locale or check if the locale is a given value: -->
현재 애플리케이션의 로케일이 무엇인지 확인하거나, 특정 로케일과 일치하는지 확인할 때는 `App` 파사드의 `currentLocale` 및 `isLocale` 메서드를 사용할 수 있습니다.

```
use Illuminate\Support\Facades\App;

$locale = App::currentLocale();

if (App::isLocale('en')) {
    // ...
}
```

<a name="pluralization-language"></a>
<!-- ### Pluralization Language -->
### Pluralization Language

<!-- You may instruct Laravel's "pluralizer", which is used by Eloquent and other portions of the framework to convert singular strings to plural strings, to use a language other than English. This may be accomplished by invoking the `useLanguage` method within the `boot` method of one of your application's service providers. The pluralizer's currently supported languages are: `french`, `norwegian-bokmal`, `portuguese`, `spanish`, and `turkish`: -->
Eloquent 등 Laravel의 여러 내부 기능에서 단수 문자열을 복수로 변환할 때 사용하는 "pluralizer(복수형 변환기)"의 언어를 영문이 아닌 다른 언어로 지정할 수 있습니다. 이 작업은 애플리케이션의 서비스 프로바이더 클래스에서 `boot` 메서드 안에서 `useLanguage` 메서드를 호출해 설정합니다. 현재 복수형 변환기에서 지원하는 언어는 `french`, `norwegian-bokmal`, `portuguese`, `spanish`, `turkish`입니다.

```
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
> 복수형 변환기 언어를 커스터마이즈할 경우, Eloquent 모델의 [table names](/docs/10.x/eloquent#table-names)을 명시적으로 지정하는 것이 좋습니다.

<a name="defining-translation-strings"></a>
<!-- ## Defining Translation Strings -->
## Defining Translation Strings

<a name="using-short-keys"></a>
<!-- ### Using Short Keys -->
### Using Short Keys

<!-- Typically, translation strings are stored in files within the `lang` directory. Within this directory, there should be a subdirectory for each language supported by your application. This is the approach Laravel uses to manage translation strings for built-in Laravel features such as validation error messages: -->
일반적으로 번역 문자열은 `lang` 디렉터리 내의 언어 파일들에 저장합니다. 이 디렉터리 안에는 애플리케이션에서 지원하는 언어별 하위 디렉터리가 있어야 합니다. 이 방법은 Laravel의 내장 기능(예: 유효성 검증 오류 메시지 등)에서 사용하는 번역 문자열을 관리하는 방식입니다.


```
/lang
    /en
        messages.php
    /es
        messages.php
```


<!-- All language files return an array of keyed strings. For example: -->
모든 언어 파일은 키가 할당된 문자열 배열을 반환해야 합니다. 예를 들면 다음과 같습니다.

```
<?php

// lang/en/messages.php

return [
    'welcome' => 'Welcome to our application!',
];
```

> [!WARNING]
> 지역에 따라 구분되는 언어(예: ‘en_GB’)의 디렉터리 이름은 ISO 15897 규격에 따라 작성해야 합니다. 예를 들어, 영국 영어의 경우 "en-gb" 대신 "en_GB"로 디렉터리명을 지정하세요.

<a name="using-translation-strings-as-keys"></a>
<!-- ### Using Translation Strings as Keys -->
### Using Translation Strings as Keys

<!-- For applications with a large number of translatable strings, defining every string with a "short key" can become confusing when referencing the keys in your views and it is cumbersome to continually invent keys for every translation string supported by your application. -->
번역할 문자열의 수가 많은 애플리케이션의 경우, 각각의 문자열에 짧은 키(short key)를 지정하는 것이 하드코딩할 때 혼란을 일으키거나, 모든 번역 문자열마다 새로운 키를 만들어야 해서 번거로울 수 있습니다.

<!-- For this reason, Laravel also provides support for defining translation strings using the "default" translation of the string as the key. Language files that use translation strings as keys are stored as JSON files in the `lang` directory. For example, if your application has a Spanish translation, you should create a `lang/es.json` file: -->
이런 이유로, Laravel에서는 번역 문자열의 "원래 내용" 자체를 키로 사용해서 번역을 정의하는 방식도 지원합니다. 이렇게 번역 문자열을 키로 사용하는 언어 파일은 `lang` 디렉터리 내에 JSON 파일로 저장됩니다. 예를 들어, 스페인어 번역이 필요한 경우 `lang/es.json` 파일을 생성할 수 있습니다.

```json
{
    "I love programming.": "Me encanta programar."
}
```

<!-- #### Key / File Conflicts -->
#### Key / File Conflicts

<!-- You should not define translation string keys that conflict with other translation filenames. For example, translating `__('Action')` for the "NL" locale while a `nl/action.php` file exists but a `nl.json` file does not exist will result in the translator returning the entire contents of `nl/action.php`. -->
다른 번역 파일 이름과 충돌하는 번역 문자열 키를 절대 정의하지 마십시오. 예를 들어, "NL" 로케일에서 `__('Action')`을 번역하려 할 때 `nl/action.php` 파일이 있는 상태에서 `nl.json` 파일이 없다면, 번역기는 `nl/action.php` 전체 내용을 반환할 수 있습니다.

<a name="retrieving-translation-strings"></a>
<!-- ## Retrieving Translation Strings -->
## Retrieving Translation Strings

<!-- You may retrieve translation strings from your language files using the `__` helper function. If you are using "short keys" to define your translation strings, you should pass the file that contains the key and the key itself to the `__` function using "dot" syntax. For example, let's retrieve the `welcome` translation string from the `lang/en/messages.php` language file: -->
`__` 헬퍼 함수를 사용해서 언어 파일에서 번역 문자열을 가져올 수 있습니다. 만약 짧은 키(short key) 방식으로 번역 문자열을 정의했다면, 키가 포함된 파일과 키 자체를 "닷(dot)" 문법으로 `__` 함수에 전달해야 합니다. 예를 들어, `lang/en/messages.php` 파일에 들어 있는 `welcome` 번역 문자열을 가져오려면 다음과 같이 할 수 있습니다.

```
echo __('messages.welcome');
```

<!-- If the specified translation string does not exist, the `__` function will return the translation string key. So, using the example above, the `__` function would return `messages.welcome` if the translation string does not exist. -->
만약 요청한 번역 문자열이 존재하지 않을 경우, `__` 함수는 번역 문자열의 키를 그대로 반환합니다. 위 예시에서 번역 문자열이 없으면 `__` 함수는 `messages.welcome`을 반환합니다.

<!--  If you are using your [default translation strings as your translation keys](#using-translation-strings-as-keys), you should pass the default translation of your string to the `__` function; -->
[default translation strings as your translation keys](#using-translation-strings-as-keys)을 활용하는 경우, 문자열의 기본값(원본 내용)을 `__` 함수에 그대로 전달하면 됩니다.

```
echo __('I love programming.');
```

<!-- Again, if the translation string does not exist, the `__` function will return the translation string key that it was given. -->
이 역시 마찬가지로, 번역 문자열이 존재하지 않으면 `__` 함수는 전달받은 번역 문자열 키를 그대로 반환합니다.

<!-- If you are using the [Blade templating engine](/docs/10.x/blade), you may use the `{{ }}` echo syntax to display the translation string: -->
[Blade templating engine](/docs/10.x/blade)을 사용할 때는 `{{ }}` 이코(echo) 문법으로 번역 문자열을 화면에 출력할 수 있습니다.

```
{{ __('messages.welcome') }}
```

<a name="replacing-parameters-in-translation-strings"></a>
<!-- ### Replacing Parameters in Translation Strings -->
### Replacing Parameters in Translation Strings

<!-- If you wish, you may define placeholders in your translation strings. All placeholders are prefixed with a `:`. For example, you may define a welcome message with a placeholder name: -->
번역 문자열에서 플레이스홀더(placeholder, 자리 표시자)를 사용할 수 있습니다. 플레이스홀더는 항상 `:` 문자로 시작합니다. 예를 들어, 사용자 이름이 들어갈 환영 메시지는 다음과 같이 작성할 수 있습니다.

```
'welcome' => 'Welcome, :name',
```

<!-- To replace the placeholders when retrieving a translation string, you may pass an array of replacements as the second argument to the `__` function: -->
번역 문자열을 가져올 때 치환할 값은 `__` 함수의 두 번째 인자로 배열 형식으로 전달하면, 해당 플레이스홀더가 해당 값으로 치환됩니다.

```
echo __('messages.welcome', ['name' => 'dayle']);
```

<!-- If your placeholder contains all capital letters, or only has its first letter capitalized, the translated value will be capitalized accordingly: -->
플레이스홀더가 모두 대문자이거나 첫 글자만 대문자인 경우, 치환되는 값 역시 해당 형식에 맞춰 집어넣어집니다.

```
'welcome' => 'Welcome, :NAME', // Welcome, DAYLE
'goodbye' => 'Goodbye, :Name', // Goodbye, Dayle
```

<a name="object-replacement-formatting"></a>
<!-- #### Object Replacement Formatting -->
#### Object Replacement Formatting

<!-- If you attempt to provide an object as a translation placeholder, the object's `__toString` method will be invoked. The [`__toString`](https://www.php.net/manual/en/language.oop5.magic.php#object.tostring) method is one of PHP's built-in "magic methods". However, sometimes you may not have control over the `__toString` method of a given class, such as when the class that you are interacting with belongs to a third-party library. -->
플레이스홀더 값으로 객체를 전달하면, 해당 객체의 `__toString` 메서드가 호출됩니다. [`__toString`](https://www.php.net/manual/en/language.oop5.magic.php#object.tostring) 메서드는 PHP의 매직 메서드 중 하나입니다. 하지만 때로는, 사용하는 클래스가 외부 라이브러리 소속 등으로 인해 여러분이 `__toString` 메서드를 직접 제어할 수 없는 경우가 있을 수 있습니다.

<!-- In these cases, Laravel allows you to register a custom formatting handler for that particular type of object. To accomplish this, you should invoke the translator's `stringable` method. The `stringable` method accepts a closure, which should type-hint the type of object that it is responsible for formatting. Typically, the `stringable` method should be invoked within the `boot` method of your application's `AppServiceProvider` class: -->
이럴 때는 Laravel의 커스텀 포맷팅 핸들러를 등록할 수 있습니다. 이를 위해서는 번역기의 `stringable` 메서드를 사용하면 됩니다. `stringable` 메서드는 클로저(익명 함수)를 인자로 받으며, 이 클로저는 포맷팅할 객체 타입을 타입힌트로 지정해야 합니다. 보통 `stringable` 메서드는 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드에서 호출합니다.

```
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
복수형 표현은 언어마다 규칙이 달라 복잡하지만, Laravel에서는 복수형 규칙에 따라 다른 방식으로 문자열을 번역할 수 있도록 도와줍니다. `|` 기호를 사용해 단수형과 복수형을 구분할 수 있습니다.

```
'apples' => 'There is one apple|There are many apples',
```

<!-- Of course, pluralization is also supported when using [translation strings as keys](#using-translation-strings-as-keys): -->
[translation strings as keys](#using-translation-strings-as-keys)을 사용할 때도 복수형 처리를 지원합니다.

```json
{
    "There is one apple|There are many apples": "Hay una manzana|Hay muchas manzanas"
}
```

<!-- You may even create more complex pluralization rules which specify translation strings for multiple ranges of values: -->
또한 복수형 규칙을 더 세밀하게 만들어, 값의 범위별로 여러 개의 번역 문자열을 지정할 수도 있습니다.

```
'apples' => '{0} There are none|[1,19] There are some|[20,*] There are many',
```

<!-- After defining a translation string that has pluralization options, you may use the `trans_choice` function to retrieve the line for a given "count". In this example, since the count is greater than one, the plural form of the translation string is returned: -->
복수형 옵션이 포함된 번역 문자열을 정의한 후에는, `trans_choice` 함수를 사용해 원하는 "개수"에 맞는 번역 문자열을 가져올 수 있습니다. 예시에서, 개수가 1보다 크다면 복수형이 반환됩니다.

```
echo trans_choice('messages.apples', 10);
```

<!-- You may also define placeholder attributes in pluralization strings. These placeholders may be replaced by passing an array as the third argument to the `trans_choice` function: -->
복수형 번역문에서 플레이스홀더 속성도 정의할 수 있습니다. `trans_choice` 함수의 세 번째 인자로 치환할 값의 배열을 넘기면, 해당 플레이스홀더가 값으로 치환됩니다.

```
'minutes_ago' => '{1} :value minute ago|[2,*] :value minutes ago',

echo trans_choice('time.minutes_ago', 5, ['value' => 5]);
```

<!-- If you would like to display the integer value that was passed to the `trans_choice` function, you may use the built-in `:count` placeholder: -->
`trans_choice` 함수에 전달한 정수 값을 번역 결과에 표시하고 싶을 때는 내장 플레이스홀더인 `:count`를 사용할 수 있습니다.

```
'apples' => '{0} There are none|{1} There is one|[2,*] There are :count',
```

<a name="overriding-package-language-files"></a>
<!-- ## Overriding Package Language Files -->
## Overriding Package Language Files

<!-- Some packages may ship with their own language files. Instead of changing the package's core files to tweak these lines, you may override them by placing files in the `lang/vendor/{package}/{locale}` directory. -->
일부 패키지는 자체 언어 파일을 함께 제공합니다. 패키지의 기본 파일을 직접 변경하지 않고도 번역 내용을 수정하려면, 여러분의 프로젝트의 `lang/vendor/{package}/{locale}` 경로에 오버라이드할 파일을 추가하면 됩니다.

<!-- So, for example, if you need to override the English translation strings in `messages.php` for a package named `skyrim/hearthfire`, you should place a language file at: `lang/vendor/hearthfire/en/messages.php`. Within this file, you should only define the translation strings you wish to override. Any translation strings you don't override will still be loaded from the package's original language files. -->
예를 들어, `skyrim/hearthfire`라는 패키지의 영어 `messages.php` 번역 문자열을 오버라이드하려면, `lang/vendor/hearthfire/en/messages.php` 파일을 생성하세요. 이 파일에는 오버라이드하고 싶은 문자열만 정의하면 됩니다. 오버라이드하지 않은 번역 문자열은 패키지의 원본 언어 파일에서 계속해서 불러와집니다.