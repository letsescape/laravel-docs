<!-- # Localization -->
# Localization

- [Introduction](#introduction)
    - [Configuring The Locale](#configuring-the-locale)
- [Defining Translation Strings](#defining-translation-strings)
    - [Using Short Keys](#using-short-keys)
    - [Using Translation Strings As Keys](#using-translation-strings-as-keys)
- [Retrieving Translation Strings](#retrieving-translation-strings)
    - [Replacing Parameters In Translation Strings](#replacing-parameters-in-translation-strings)
    - [Pluralization](#pluralization)
- [Overriding Package Language Files](#overriding-package-language-files)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Laravel's localization features provide a convenient way to retrieve strings in various languages, allowing you to easily support multiple languages within your application. -->
Laravel의 로컬라이제이션(localization) 기능을 사용하면 다양한 언어의 문자열을 편리하게 가져올 수 있어, 애플리케이션에서 여러 언어를 쉽게 지원할 수 있습니다.

<!-- Laravel provides two ways to manage translation strings. First, language strings may be stored in files within the `resources/lang` directory. Within this directory, there may be subdirectories for each language supported by the application. This is the approach Laravel uses to manage translation strings for built-in Laravel features such as validation error messages: -->
Laravel에서는 번역 문자열을 관리하는 두 가지 방법을 제공합니다. 첫 번째는 `resources/lang` 디렉터리 내에 파일 형태로 언어 문자열을 저장하는 방식입니다. 이 디렉터리 내에는 애플리케이션이 지원하는 각 언어별로 서브디렉터리가 있을 수 있습니다. Laravel은 기본적으로 유효성 검사 에러 메시지 등 자체 제공 기능의 번역 문자열을 이 방식으로 관리합니다.


```
/resources
    /lang
        /en
            messages.php
        /es
            messages.php
```


<!-- Or, translation strings may be defined within JSON files that are placed within the `resources/lang` directory. When taking this approach, each language supported by your application would have a corresponding JSON file within this directory. This approach is recommended for application's that have a large number of translatable strings: -->
또는, 번역 문자열을 `resources/lang` 디렉터리 내의 JSON 파일에 정의할 수도 있습니다. 이 방법을 사용하면 애플리케이션에서 지원하는 각 언어별로 해당 언어의 JSON 파일이 필요합니다. 다수의 번역 문자열을 지원해야 하는 애플리케이션에는 이 방법을 권장합니다.


```
/resources
    /lang
        en.json
        es.json
```


<!-- We'll discuss each approach to managing translation strings within this documentation. -->
이 문서에서는 위에서 설명한 각각의 번역 문자열 관리 방식을 다룰 것입니다.

<a name="configuring-the-locale"></a>
<!-- ### Configuring The Locale -->
### Configuring The Locale

<!-- The default language for your application is stored in the `config/app.php` configuration file's `locale` configuration option. You are free to modify this value to suit the needs of your application. -->
애플리케이션의 기본 언어(로케일)는 `config/app.php` 설정 파일의 `locale` 항목에 저장되어 있습니다. 이 값은 애플리케이션의 요구에 맞게 자유롭게 수정할 수 있습니다.

<!-- You may modify the default language for a single HTTP request at runtime using the `setLocale` method provided by the `App` facade: -->
실행 시간(runtime) 중 단일 HTTP 요청에 대해 기본 언어를 동적으로 변경하려면, `App` 파사드가 제공하는 `setLocale` 메서드를 사용할 수 있습니다.

```
use Illuminate\Support\Facades\App;

Route::get('/greeting/{locale}', function ($locale) {
    if (! in_array($locale, ['en', 'es', 'fr'])) {
        abort(400);
    }

    App::setLocale($locale);

    //
});
```

<!-- You may configure a "fallback language", which will be used when the active language does not contain a given translation string. Like the default language, the fallback language is also configured in the `config/app.php` configuration file: -->
현재 언어로 제공되지 않은 번역 문자열이 있을 때 사용할 수 있는 "대체 언어(fallback language)"도 설정할 수 있습니다. 이 역시 `config/app.php` 설정 파일에서 지정합니다.

```
'fallback_locale' => 'en',
```

<a name="determining-the-current-locale"></a>
<!-- #### Determining The Current Locale -->
#### Determining The Current Locale

<!-- You may use the `currentLocale` and `isLocale` methods on the `App` facade to determine the current locale or check if the locale is a given value: -->
현재 애플리케이션의 로케일을 확인하거나, 지정한 값과 일치하는지 확인하려면 `App` 파사드의 `currentLocale` 및 `isLocale` 메서드를 사용할 수 있습니다.

```
use Illuminate\Support\Facades\App;

$locale = App::currentLocale();

if (App::isLocale('en')) {
    //
}
```

<a name="defining-translation-strings"></a>
<!-- ## Defining Translation Strings -->
## Defining Translation Strings

<a name="using-short-keys"></a>
<!-- ### Using Short Keys -->
### Using Short Keys

<!-- Typically, translation strings are stored in files within the `resources/lang` directory. Within this directory, there should be a subdirectory for each language supported by your application. This is the approach Laravel uses to manage translation strings for built-in Laravel features such as validation error messages: -->
일반적으로 번역 문자열은 `resources/lang` 디렉터리 내 파일에 저장합니다. 이 디렉터리 내에는 애플리케이션에서 지원하는 각 언어별로 하위 디렉터리가 필요합니다. Laravel 자체의 유효성 검사 에러 메시지 등 내장 기능의 번역 문자열 역시 이 방식을 사용합니다.


```
/resources
    /lang
        /en
            messages.php
        /es
            messages.php
```


<!-- All language files return an array of keyed strings. For example: -->
모든 언어 파일은 키(key)와 문자열로 구성된 배열을 반환합니다. 예시:

```
<?php

// resources/lang/en/messages.php

return [
    'welcome' => 'Welcome to our application!',
];
```

> [!NOTE]
> 지역(territory)별로 분리되는 언어의 경우, 언어 디렉터리 이름은 ISO 15897 표준에 따라 지정해야 합니다. 예를 들어, 영국 영어는 "en_GB"로, "en-gb"가 아닌 "en_GB"를 사용해야 합니다.

<a name="using-translation-strings-as-keys"></a>
<!-- ### Using Translation Strings As Keys -->
### Using Translation Strings As Keys

<!-- For applications with a large number of translatable strings, defining every string with a "short key" can become confusing when referencing the keys in your views and it is cumbersome to continually invent keys for every translation string supported by your application. -->
번역해야 할 문자열이 많은 애플리케이션에서는 각각의 문자열에 "짧은 키"를 부여하여 관리하는 것이 뷰에서 키를 참조할 때 혼동을 줄 수 있고, 계속해서 새로운 키를 만드는 것이 번거로울 수 있습니다.

<!-- For this reason, Laravel also provides support for defining translation strings using the "default" translation of the string as the key. Translation files that use translation strings as keys are stored as JSON files in the `resources/lang` directory. For example, if your application has a Spanish translation, you should create a `resources/lang/es.json` file: -->
이러한 경우를 위해, Laravel에서는 번역 문자열의 "기본값" 자체를 키로 사용하는 방식을 지원합니다. 이 방법을 사용할 때 번역 파일은 `resources/lang` 디렉터리의 JSON 파일로 저장됩니다. 예를 들어, 스페인어 번역을 위해서는 `resources/lang/es.json` 파일을 생성합니다.

```js
{
    "I love programming.": "Me encanta programar."
}
```

<!-- #### Key / File Conflicts -->
#### Key / File Conflicts

<!-- You should not define translation string keys that conflict with other translation filenames. For example, translating `__('Action')` for the "NL" locale while a `nl/action.php` file exists but a `nl.json` file does not exist will result in the translator returning the contents of `nl/action.php`. -->
다른 번역 파일명과 충돌하는 키를 정의하지 않아야 합니다. 예를 들어, "NL" 로케일에서 `__('Action')`을 번역하고자 할 때, 만약 `nl/action.php` 파일이 존재하고 `nl.json` 파일이 없다면, 트랜스레이터는 `nl/action.php` 내용을 반환하게 됩니다.

<a name="retrieving-translation-strings"></a>
<!-- ## Retrieving Translation Strings -->
## Retrieving Translation Strings

<!-- You may retrieve translation strings from your language files using the `__` helper function. If you are using "short keys" to define your translation strings, you should pass the file that contains the key and the key itself to the `__` function using "dot" syntax. For example, let's retrieve the `welcome` translation string from the `resources/lang/en/messages.php` language file: -->
번역 문자열은 `__` 헬퍼 함수를 통해 언어 파일에서 가져올 수 있습니다. "짧은 키" 형식으로 번역 문자열을 정의한 경우, 해당 키가 들어 있는 파일과 키를 "점(dot) 문법"으로 `__` 함수에 전달해야 합니다. 예를 들어, `resources/lang/en/messages.php` 파일의 `welcome` 번역 문자열을 가져오려면 다음과 같이 작성합니다.

```
echo __('messages.welcome');
```

<!-- If the specified translation string does not exist, the `__` function will return the translation string key. So, using the example above, the `__` function would return `messages.welcome` if the translation string does not exist. -->
지정한 번역 문자열이 존재하지 않을 경우, `__` 함수는 번역 문자열 키를 반환합니다. 따라서 위 예시에서 해당 문자열이 없으면 `__` 함수는 `messages.welcome`을 반환합니다.

<!--  If you are using your [default translation strings as your translation keys](#using-translation-strings-as-keys), you should pass the default translation of your string to the `__` function; -->
[default translation strings as your translation keys](#using-translation-strings-as-keys)을 사용할 때에는 기본 번역 문자열을 그대로 `__` 함수에 전달하면 됩니다.

```
echo __('I love programming.');
```

<!-- Again, if the translation string does not exist, the `__` function will return the translation string key that it was given. -->
마찬가지로, 번역 문자열이 존재하지 않으면 `__` 함수는 전달받은 번역 문자열 키를 그대로 반환합니다.

<!-- If you are using the [Blade templating engine](/docs/8.x/blade), you may use the `{{ }}` echo syntax to display the translation string: -->
[Blade templating engine](/docs/8.x/blade)을 사용하는 경우, `{{ }}` 출력 구문을 사용해 번역 문자열을 표시할 수 있습니다.

```
{{ __('messages.welcome') }}
```

<a name="replacing-parameters-in-translation-strings"></a>
<!-- ### Replacing Parameters In Translation Strings -->
### Replacing Parameters In Translation Strings

<!-- If you wish, you may define placeholders in your translation strings. All placeholders are prefixed with a `:`. For example, you may define a welcome message with a placeholder name: -->
필요에 따라 번역 문자열 안에 플레이스홀더(placeholder)를 정의할 수 있습니다. 모든 플레이스홀더는 앞에 `:`가 붙습니다. 예를 들어, 이름 플레이스홀더를 포함한 환영 메시지는 다음과 같이 작성합니다.

```
'welcome' => 'Welcome, :name',
```

<!-- To replace the placeholders when retrieving a translation string, you may pass an array of replacements as the second argument to the `__` function: -->
번역 문자열을 가져올 때 플레이스홀더를 실제 값으로 치환하려면, `__` 함수의 두 번째 인자로 치환할 값을 배열로 전달합니다.

```
echo __('messages.welcome', ['name' => 'dayle']);
```

<!-- If your placeholder contains all capital letters, or only has its first letter capitalized, the translated value will be capitalized accordingly: -->
플레이스홀더가 모두 대문자이거나, 첫 글자만 대문자인 경우 주어진 값도 이에 맞게 대문자로 대체됩니다.

```
'welcome' => 'Welcome, :NAME', // Welcome, DAYLE
'goodbye' => 'Goodbye, :Name', // Goodbye, Dayle
```

<a name="pluralization"></a>
<!-- ### Pluralization -->
### Pluralization

<!-- Pluralization is a complex problem, as different languages have a variety of complex rules for pluralization; however, Laravel can help you translate strings differently based on pluralization rules that you define. Using a `|` character, you may distinguish singular and plural forms of a string: -->
복수형 처리(pluralization)는 언어마다 규칙이 다양하기 때문에 복잡할 수 있습니다. 하지만 Laravel을 사용하면 직접 정의한 복수형 규칙에 따라 번역 문자열을 다르게 출력할 수 있습니다. 문자열에 `|` 문자를 사용하여 단수와 복수 형식을 구분할 수 있습니다.

```
'apples' => 'There is one apple|There are many apples',
```

<!-- Of course, pluralization is also supported when using [translation strings as keys](#using-translation-strings-as-keys): -->
[translation strings as keys](#using-translation-strings-as-keys)에서도 복수형 처리가 지원됩니다.

```js
{
    "There is one apple|There are many apples": "Hay una manzana|Hay muchas manzanas"
}
```

<!-- You may even create more complex pluralization rules which specify translation strings for multiple ranges of values: -->
또한, 값의 범위에 따라 여러 조건으로 복수형을 처리할 수도 있습니다.

```
'apples' => '{0} There are none|[1,19] There are some|[20,*] There are many',
```

<!-- After defining a translation string that has pluralization options, you may use the `trans_choice` function to retrieve the line for a given "count". In this example, since the count is greater than one, the plural form of the translation string is returned: -->
복수형 옵션이 정의된 번역 문자열은 `trans_choice` 함수를 사용해 지정한 "개수(count)"에 맞는 형식으로 가져올 수 있습니다. 아래 예시에서 count가 1보다 크기 때문에 복수형이 반환됩니다.

```
echo trans_choice('messages.apples', 10);
```

<!-- You may also define placeholder attributes in pluralization strings. These placeholders may be replaced by passing an array as the third argument to the `trans_choice` function: -->
복수형 번역 문자열 내부에 플레이스홀더 속성도 정의할 수 있습니다. 이 경우 `trans_choice` 함수의 세 번째 인자로 치환 값을 배열로 전달하면 됩니다.

```
'minutes_ago' => '{1} :value minute ago|[2,*] :value minutes ago',

echo trans_choice('time.minutes_ago', 5, ['value' => 5]);
```

<!-- If you would like to display the integer value that was passed to the `trans_choice` function, you may use the built-in `:count` placeholder: -->
`trans_choice` 함수에 넘긴 정수값을 번역 문자열 내에서 그대로 표시하려면 기본 제공되는 `:count` 플레이스홀더를 사용할 수 있습니다.

```
'apples' => '{0} There are none|{1} There is one|[2,*] There are :count',
```

<a name="overriding-package-language-files"></a>
<!-- ## Overriding Package Language Files -->
## Overriding Package Language Files

<!-- Some packages may ship with their own language files. Instead of changing the package's core files to tweak these lines, you may override them by placing files in the `resources/lang/vendor/{package}/{locale}` directory. -->
일부 패키지는 자체 언어 파일을 포함하고 있을 수 있습니다. 이런 경우, 패키지의 핵심 파일을 직접 수정하는 대신, `resources/lang/vendor/{package}/{locale}` 디렉터리 내에 파일을 생성하여 원하는 번역 문자열만 재정의할 수 있습니다.

<!-- So, for example, if you need to override the English translation strings in `messages.php` for a package named `skyrim/hearthfire`, you should place a language file at: `resources/lang/vendor/hearthfire/en/messages.php`. Within this file, you should only define the translation strings you wish to override. Any translation strings you don't override will still be loaded from the package's original language files. -->
예를 들어, `skyrim/hearthfire`라는 패키지의 `messages.php` 영어 번역 문자열을 재정의하고 싶은 경우, `resources/lang/vendor/hearthfire/en/messages.php`에 번역 파일을 작성하면 됩니다. 이 파일에는 오버라이드하고 싶은 번역 문자열만 정의하면 됩니다. 정의하지 않은 번역 문자열은 패키지의 원본 언어 파일에서 계속 로드됩니다.
