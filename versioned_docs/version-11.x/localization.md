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
> 기본적으로 Laravel 애플리케이션 스캐폴딩에는 `lang` 디렉터리가 포함되어 있지 않습니다. Laravel의 언어 파일을 직접 커스터마이징하려면 `lang:publish` 아티즌 명령어를 사용해 퍼블리싱할 수 있습니다.

<!-- Laravel's localization features provide a convenient way to retrieve strings in various languages, allowing you to easily support multiple languages within your application. -->
Laravel의 로컬라이제이션(Localization, 다국어 지원) 기능은 여러 언어로 문자열을 손쉽게 가져올 수 있도록 해주어, 애플리케이션에서 다양한 언어를 쉽게 지원할 수 있게 해줍니다.

<!-- Laravel provides two ways to manage translation strings. First, language strings may be stored in files within the application's `lang` directory. Within this directory, there may be subdirectories for each language supported by the application. This is the approach Laravel uses to manage translation strings for built-in Laravel features such as validation error messages: -->
Laravel에서는 번역 문자열을 관리하는 두 가지 방법을 제공합니다. 첫 번째는 애플리케이션의 `lang` 디렉터리 내 파일에 언어 문자열을 저장하는 방식입니다. 이 디렉터리 안에는 애플리케이션이 지원하는 각 언어별로 하위 디렉터리가 있을 수 있습니다. 이 방식은 유효성 검사 오류 메시지와 같은 Laravel 내장 기능의 번역 문자열을 관리하는 데 사용됩니다.


```
/lang
    /en
        messages.php
    /es
        messages.php
```


<!-- Or, translation strings may be defined within JSON files that are placed within the `lang` directory. When taking this approach, each language supported by your application would have a corresponding JSON file within this directory. This approach is recommended for applications that have a large number of translatable strings: -->
또는, `lang` 디렉터리 내에 JSON 파일을 만들어 번역 문자열을 관리할 수도 있습니다. 이 방식을 사용할 때는, 애플리케이션에서 지원하는 각 언어마다 해당 언어의 JSON 파일을 이 디렉터리에 두면 됩니다. 번역해야 할 문자열이 많은 애플리케이션이라면 이 방식을 권장합니다.

```
/lang
    en.json
    es.json
```

<!-- We'll discuss each approach to managing translation strings within this documentation. -->
본 문서에서는 위 두 가지 번역 문자열 관리 방식을 자세히 다뤄보겠습니다.

<a name="publishing-the-language-files"></a>
<!-- ### Publishing the Language Files -->
### Publishing the Language Files

<!-- By default, the Laravel application skeleton does not include the `lang` directory. If you would like to customize Laravel's language files or create your own, you should scaffold the `lang` directory via the `lang:publish` Artisan command. The `lang:publish` command will create the `lang` directory in your application and publish the default set of language files used by Laravel: -->
기본적으로 Laravel 애플리케이션 기본 구조에는 `lang` 디렉터리가 포함되어 있지 않습니다. Laravel의 언어 파일을 커스터마이즈하거나 직접 새로 만들고 싶다면, `lang:publish` 아티즌 명령어를 실행해서 `lang` 디렉터리를 만들어야 합니다. `lang:publish` 명령어는 애플리케이션에 `lang` 디렉터리를 생성하고, Laravel에서 사용하는 기본 언어 파일들을 퍼블리싱합니다.

```shell
php artisan lang:publish
```

<a name="configuring-the-locale"></a>
<!-- ### Configuring the Locale -->
### Configuring the Locale

<!-- The default language for your application is stored in the `config/app.php` configuration file's `locale` configuration option, which is typically set using the `APP_LOCALE` environment variable. You are free to modify this value to suit the needs of your application. -->
애플리케이션의 기본 언어는 `config/app.php` 설정 파일의 `locale` 옵션에 저장되어 있습니다. 이 값은 일반적으로 `APP_LOCALE` 환경 변수로 설정합니다. 애플리케이션에 적합한 언어로 자유롭게 변경해서 사용할 수 있습니다.

<!-- You may also configure a "fallback language", which will be used when the default language does not contain a given translation string. Like the default language, the fallback language is also configured in the `config/app.php` configuration file, and its value is typically set using the `APP_FALLBACK_LOCALE` environment variable. -->
또한, 기본 언어에 해당하는 번역 문자열이 없는 경우 사용될 "폴백(fallback) 언어"도 설정할 수 있습니다. 폴백 언어도 마찬가지로 `config/app.php` 설정 파일에서 `APP_FALLBACK_LOCALE` 환경 변수로 지정합니다.

<!-- You may modify the default language for a single HTTP request at runtime using the `setLocale` method provided by the `App` facade: -->
특정 HTTP 요청에 한 해 런타임에서 기본 언어를 변경하고 싶다면, `App` 파사드의 `setLocale` 메서드를 사용할 수 있습니다.

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

<a name="determining-the-current-locale"></a>
<!-- #### Determining the Current Locale -->
#### Determining the Current Locale

<!-- You may use the `currentLocale` and `isLocale` methods on the `App` facade to determine the current locale or check if the locale is a given value: -->
현재 애플리케이션에서 어떤 로케일이 사용되고 있는지 확인하거나, 특정 로케일과 일치하는지 확인하려면 `App` 파사드의 `currentLocale` 및 `isLocale` 메서드를 사용할 수 있습니다.

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
Laravel의 "플루럴라이저(pluralizer)"는 Eloquent나 프레임워크 내 여러 부분에서 단어의 단수형을 복수형으로 변환할 때 사용됩니다. 이 플루럴라이저가 영어가 아닌 다른 언어를 사용하도록 지정할 수 있습니다. 이를 위해서는 애플리케이션 서비스 프로바이더 중 하나의 `boot` 메서드에서 `useLanguage` 메서드를 호출하면 됩니다. 플루럴라이저에서 현재 지원하는 언어는 다음과 같습니다: `french`, `norwegian-bokmal`, `portuguese`, `spanish`, `turkish`.

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
> 플루럴라이저 언어를 커스터마이즈했다면, Eloquent 모델의 [table names](/docs/11.x/eloquent#table-names)을 반드시 명시적으로 정의해야 합니다.

<a name="defining-translation-strings"></a>
<!-- ## Defining Translation Strings -->
## Defining Translation Strings

<a name="using-short-keys"></a>
<!-- ### Using Short Keys -->
### Using Short Keys

<!-- Typically, translation strings are stored in files within the `lang` directory. Within this directory, there should be a subdirectory for each language supported by your application. This is the approach Laravel uses to manage translation strings for built-in Laravel features such as validation error messages: -->
일반적으로 번역 문자열은 `lang` 디렉터리 내 파일에 저장합니다. 이 디렉터리 안에는 애플리케이션이 지원하는 각 언어별로 하위 디렉터리를 두는 것이 좋습니다. 이 방식은 Laravel의 내장 기능(예: 유효성 검사 오류 메시지 등)의 번역 문자열을 관리할 때 사용됩니다.


```
/lang
    /en
        messages.php
    /es
        messages.php
```


<!-- All language files return an array of keyed strings. For example: -->
모든 언어 파일은 키(key)와 번역 문자열로 이루어진 배열을 반환해야 합니다. 예를 들어 아래와 같습니다.

```
<?php

// lang/en/messages.php

return [
    'welcome' => 'Welcome to our application!',
];
```

> [!WARNING]
> 국가/지역에 따라 차이가 있는 언어에는 ISO 15897 규격에 맞춰 폴더 이름을 정해야 합니다. 예를 들어 영국식 영어는 "en-gb" 대신 "en_GB"로 폴더명을 만들어야 합니다.

<a name="using-translation-strings-as-keys"></a>
<!-- ### Using Translation Strings as Keys -->
### Using Translation Strings as Keys

<!-- For applications with a large number of translatable strings, defining every string with a "short key" can become confusing when referencing the keys in your views and it is cumbersome to continually invent keys for every translation string supported by your application. -->
번역해야 할 문자열이 많은 애플리케이션에서는, 모든 문자열마다 "짧은 키"를 만들어 관리하기가 번거롭고, 실제 뷰에서 키를 참고할 때 혼란을 겪을 수도 있습니다. 그래서 Laravel은 "기본 번역 문자열 자체를 키"로 사용해 번역을 관리하는 방법도 지원합니다.

<!-- For this reason, Laravel also provides support for defining translation strings using the "default" translation of the string as the key. Language files that use translation strings as keys are stored as JSON files in the `lang` directory. For example, if your application has a Spanish translation, you should create a `lang/es.json` file: -->
이 방식을 사용하는 번역 파일은 `lang` 디렉터리에 JSON 파일로 저장됩니다. 예를 들어, 애플리케이션에 스페인어 번역이 있다면 `lang/es.json` 파일을 만들어야 합니다.

```json
{
    "I love programming.": "Me encanta programar."
}
```

<!-- #### Key / File Conflicts -->
#### Key / File Conflicts

<!-- You should not define translation string keys that conflict with other translation filenames. For example, translating `__('Action')` for the "NL" locale while a `nl/action.php` file exists but a `nl.json` file does not exist will result in the translator returning the entire contents of `nl/action.php`. -->
다른 번역 파일 이름과 충돌하는 번역 키를 만들면 안 됩니다. 예를 들어 "NL" 로케일에 대해 `__('Action')`을 번역하려고 할 때, `nl/action.php` 파일이 존재하지만 `nl.json` 파일이 없다면, 번역기는 `nl/action.php` 파일의 모든 내용을 반환하게 됩니다.

<a name="retrieving-translation-strings"></a>
<!-- ## Retrieving Translation Strings -->
## Retrieving Translation Strings

<!-- You may retrieve translation strings from your language files using the `__` helper function. If you are using "short keys" to define your translation strings, you should pass the file that contains the key and the key itself to the `__` function using "dot" syntax. For example, let's retrieve the `welcome` translation string from the `lang/en/messages.php` language file: -->
언어 파일에서 번역 문자열을 가져오려면 `__` 헬퍼 함수를 사용할 수 있습니다. 번역 문자열을 "짧은 키" 형태로 정의했다면, 해당 키를 포함하는 파일 이름과 키를 "닷(dot) 표기법"으로 `__` 함수에 전달해야 합니다. 예를 들어 `lang/en/messages.php`의 `welcome` 번역 문자열을 가져오는 방법은 다음과 같습니다.

```
echo __('messages.welcome');
```

<!-- If the specified translation string does not exist, the `__` function will return the translation string key. So, using the example above, the `__` function would return `messages.welcome` if the translation string does not exist. -->
지정한 번역 문자열이 존재하지 않을 경우, `__` 함수는 번역 문자열 키를 반환합니다. 따라서 위 예시라면 번역 문자열이 없을 때 `__` 함수는 `messages.welcome`을 반환합니다.

<!-- If you are using your [default translation strings as your translation keys](#using-translation-strings-as-keys), you should pass the default translation of your string to the `__` function; -->
만약 [default translation strings as your translation keys](#using-translation-strings-as-keys)을 쓴다면, 번역하고자 하는 원본 문자열 자체를 `__` 함수에 바로 전달하면 됩니다.

```
echo __('I love programming.');
```

<!-- Again, if the translation string does not exist, the `__` function will return the translation string key that it was given. -->
이 경우에도 번역 문자열이 존재하지 않으면 `__` 함수는 전달받은 번역 문자열 키를 그대로 반환합니다.

<!-- If you are using the [Blade templating engine](/docs/11.x/blade), you may use the `{{ }}` echo syntax to display the translation string: -->
[Blade templating engine](/docs/11.x/blade)에서는 `{{ }}`를 사용하여 번역 문자열을 화면에 표시할 수 있습니다.

```
{{ __('messages.welcome') }}
```

<a name="replacing-parameters-in-translation-strings"></a>
<!-- ### Replacing Parameters in Translation Strings -->
### Replacing Parameters in Translation Strings

<!-- If you wish, you may define placeholders in your translation strings. All placeholders are prefixed with a `:`. For example, you may define a welcome message with a placeholder name: -->
번역 문자열에 플레이스홀더(치환 변수)를 정의하고 싶다면, 플레이스홀더명 앞에 `:` 기호를 붙여 작성합니다. 예를 들어 환영 메시지에 이름 값을 넣고 싶다면 아래와 같이 작성할 수 있습니다.

```
'welcome' => 'Welcome, :name',
```

<!-- To replace the placeholders when retrieving a translation string, you may pass an array of replacements as the second argument to the `__` function: -->
번역 문자열을 가져올 때 플레이스홀더에 해당하는 값을 넣고 싶다면, `__` 함수의 두 번째 인수로 치환할 데이터를 배열 형태로 전달하면 됩니다.

```
echo __('messages.welcome', ['name' => 'dayle']);
```

<!-- If your placeholder contains all capital letters, or only has its first letter capitalized, the translated value will be capitalized accordingly: -->
플레이스홀더가 모두 대문자이거나 첫 글자만 대문자인 경우, 실제 번역값도 대문자나 첫 글자를 대문자로 치환하여 출력됩니다.

```
'welcome' => 'Welcome, :NAME', // Welcome, DAYLE
'goodbye' => 'Goodbye, :Name', // Goodbye, Dayle
```

<a name="object-replacement-formatting"></a>
<!-- #### Object Replacement Formatting -->
#### Object Replacement Formatting

<!-- If you attempt to provide an object as a translation placeholder, the object's `__toString` method will be invoked. The [`__toString`](https://www.php.net/manual/en/language.oop5.magic.php#object.tostring) method is one of PHP's built-in "magic methods". However, sometimes you may not have control over the `__toString` method of a given class, such as when the class that you are interacting with belongs to a third-party library. -->
치환값으로 객체를 전달하면, 해당 객체의 `__toString` 메서드가 호출됩니다. [`__toString`](https://www.php.net/manual/en/language.oop5.magic.php#object.tostring) 메서드는 PHP에 내장된 "매직 메서드" 중 하나입니다. 단, 서드파티 라이브러리 등 자신의 통제가 불가능한 클래스에서는 `__toString` 동작을 변경할 수 없는 경우도 있습니다.

<!-- In these cases, Laravel allows you to register a custom formatting handler for that particular type of object. To accomplish this, you should invoke the translator's `stringable` method. The `stringable` method accepts a closure, which should type-hint the type of object that it is responsible for formatting. Typically, the `stringable` method should be invoked within the `boot` method of your application's `AppServiceProvider` class: -->
이러한 경우 Laravel에서는 해당 타입의 객체를 포맷팅하는 커스텀 핸들러를 등록할 수 있습니다. 이를 위해 번역기의 `stringable` 메서드를 사용합니다. `stringable` 메서드는 클로저(익명 함수)를 인수로 받으며, 이 클로저는 포맷팅을 책임질 객체 타입을 타입힌트로 선언해야 합니다. 보통 `stringable` 메서드는 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드에서 호출합니다.

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
복수화(Pluralization)는 언어마다 규칙이 매우 복잡한 주제이지만, Laravel을 사용하면 언어별 복수화 규칙에 따라 번역할 수 있습니다. `|` 문자를 사용하여 단수 및 복수 표현을 구분할 수 있습니다.

```
'apples' => 'There is one apple|There are many apples',
```

<!-- Of course, pluralization is also supported when using [translation strings as keys](#using-translation-strings-as-keys): -->
물론, [translation strings as keys](#using-translation-strings-as-keys)에서도 복수화가 가능합니다.

```json
{
    "There is one apple|There are many apples": "Hay una manzana|Hay muchas manzanas"
}
```

<!-- You may even create more complex pluralization rules which specify translation strings for multiple ranges of values: -->
값의 범위를 지정해서 세분화된 복수화 규칙도 만들 수 있습니다.

```
'apples' => '{0} There are none|[1,19] There are some|[20,*] There are many',
```

<!-- After defining a translation string that has pluralization options, you may use the `trans_choice` function to retrieve the line for a given "count". In this example, since the count is greater than one, the plural form of the translation string is returned: -->
복수화를 위한 번역 문자열이 정의되어 있다면, `trans_choice` 함수를 사용해 "개수"에 맞는 표현을 가져올 수 있습니다. 아래 예시에서, 10과 같은 2 이상 값이 들어가면 복수형이 반환됩니다.

```
echo trans_choice('messages.apples', 10);
```

<!-- You may also define placeholder attributes in pluralization strings. These placeholders may be replaced by passing an array as the third argument to the `trans_choice` function: -->
복수화 문자열에서도 치환 변수를 사용할 수 있습니다. 이 경우, `trans_choice` 함수의 세 번째 인수로 치환할 데이터를 배열로 전달합니다.

```
'minutes_ago' => '{1} :value minute ago|[2,*] :value minutes ago',

echo trans_choice('time.minutes_ago', 5, ['value' => 5]);
```

<!-- If you would like to display the integer value that was passed to the `trans_choice` function, you may use the built-in `:count` placeholder: -->
`trans_choice` 함수에 전달한 정수 값을 그대로 표시하려면 `:count` 내장 플레이스홀더를 사용하면 됩니다.

```
'apples' => '{0} There are none|{1} There is one|[2,*] There are :count',
```

<a name="overriding-package-language-files"></a>
<!-- ## Overriding Package Language Files -->
## Overriding Package Language Files

<!-- Some packages may ship with their own language files. Instead of changing the package's core files to tweak these lines, you may override them by placing files in the `lang/vendor/{package}/{locale}` directory. -->
일부 패키지는 자체 언어 파일을 포함할 수 있습니다. 이러한 패키지의 언어 파일을 수정하고 싶다면, 패키지의 코어 파일을 직접 변경하는 대신 `lang/vendor/{package}/{locale}` 디렉터리에 파일을 두어 오버라이드(재정의)할 수 있습니다.

<!-- So, for example, if you need to override the English translation strings in `messages.php` for a package named `skyrim/hearthfire`, you should place a language file at: `lang/vendor/hearthfire/en/messages.php`. Within this file, you should only define the translation strings you wish to override. Any translation strings you don't override will still be loaded from the package's original language files. -->
예를 들어, `skyrim/hearthfire`라는 패키지에서 `messages.php`의 영문 번역 문자열만 오버라이딩하고 싶다면, `lang/vendor/hearthfire/en/messages.php`에 해당 언어 파일을 두면 됩니다. 이 파일에는 오버라이딩할 번역 문자열만 정의하면 됩니다. 오버라이딩하지 않은 번역 항목은 여전히 패키지의 원래 언어 파일에서 불러옵니다.