<!-- # Validation -->
# Validation

- [Introduction](#introduction)
- [Validation Quickstart](#validation-quickstart)
    - [Defining the Routes](#quick-defining-the-routes)
    - [Creating the Controller](#quick-creating-the-controller)
    - [Writing the Validation Logic](#quick-writing-the-validation-logic)
    - [Displaying the Validation Errors](#quick-displaying-the-validation-errors)
    - [Repopulating Forms](#repopulating-forms)
    - [A Note on Optional Fields](#a-note-on-optional-fields)
    - [Validation Error Response Format](#validation-error-response-format)
- [Form Request Validation](#form-request-validation)
    - [Creating Form Requests](#creating-form-requests)
    - [Authorizing Form Requests](#authorizing-form-requests)
    - [Customizing the Error Messages](#customizing-the-error-messages)
    - [Preparing Input for Validation](#preparing-input-for-validation)
- [Manually Creating Validators](#manually-creating-validators)
    - [Automatic Redirection](#automatic-redirection)
    - [Named Error Bags](#named-error-bags)
    - [Customizing the Error Messages](#manual-customizing-the-error-messages)
    - [Performing Additional Validation](#performing-additional-validation)
- [Working With Validated Input](#working-with-validated-input)
- [Working With Error Messages](#working-with-error-messages)
    - [Specifying Custom Messages in Language Files](#specifying-custom-messages-in-language-files)
    - [Specifying Attributes in Language Files](#specifying-attribute-in-language-files)
    - [Specifying Values in Language Files](#specifying-values-in-language-files)
- [Available Validation Rules](#available-validation-rules)
- [Conditionally Adding Rules](#conditionally-adding-rules)
- [Validating Arrays](#validating-arrays)
    - [Validating Nested Array Input](#validating-nested-array-input)
    - [Error Message Indexes and Positions](#error-message-indexes-and-positions)
- [Validating Files](#validating-files)
- [Validating Passwords](#validating-passwords)
- [Custom Validation Rules](#custom-validation-rules)
    - [Using Rule Objects](#using-rule-objects)
    - [Using Closures](#using-closures)
    - [Implicit Rules](#implicit-rules)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Laravel provides several different approaches to validate your application's incoming data. It is most common to use the `validate` method available on all incoming HTTP requests. However, we will discuss other approaches to validation as well. -->
Laravel は、アプリケーションの受信データを検証するためのいくつかの異なるアプローチを提供します。すべての受信 HTTP リクエストで使用できる `validate` メソッドを使用するのが最も一般的です。ただし、他の検証アプローチについても説明します。

<!-- Laravel includes a wide variety of convenient validation rules that you may apply to data, even providing the ability to validate if values are unique in a given database table. We'll cover each of these validation rules in detail so that you are familiar with all of Laravel's validation features. -->
Laravel には、データに適用できる便利な検証ルールが幅広く含まれており、特定のデータベーステーブル内で値が一意であるかどうかを検証する機能も提供します。 Laravel のすべての検証機能を理解できるように、これらの検証ルールのそれぞれについて詳しく説明します。

<a name="validation-quickstart"></a>
<!-- ## Validation Quickstart -->
## Validation Quickstart

<!-- To learn about Laravel's powerful validation features, let's look at a complete example of validating a form and displaying the error messages back to the user. By reading this high-level overview, you'll be able to gain a good general understanding of how to validate incoming request data using Laravel: -->
Laravel の強力な検証機能について学ぶために、フォームを検証し、ユーザーにエラー メッセージを表示する完全な例を見てみましょう。この高レベルの概要を読むことで、Laravel を使用して受信リクエスト データを検証する方法について一般的に理解できるようになります。

<a name="quick-defining-the-routes"></a>
<!-- ### Defining the Routes -->
### Defining the Routes

<!-- First, let's assume we have the following routes defined in our `routes/web.php` file: -->
まず、`routes/web.php` ファイルに次のルートが定義されていると仮定します。

```php
use App\Http\Controllers\PostController;

Route::get('/post/create', [PostController::class, 'create']);
Route::post('/post', [PostController::class, 'store']);
```

<!-- The `GET` route will display a form for the user to create a new blog post, while the `POST` route will store the new blog post in the database. -->
`GET` ルートはユーザーが新しいブログ投稿を作成するためのフォームを表示し、`POST` ルートは新しいブログ投稿をデータベースに保存します。

<a name="quick-creating-the-controller"></a>
<!-- ### Creating the Controller -->
### Creating the Controller

<!-- Next, let's take a look at a simple controller that handles incoming requests to these routes. We'll leave the `store` method empty for now: -->
次に、これらのルートへの受信リクエストを処理する単純なコントローラを見てみましょう。現時点では、`store` メソッドを空のままにしておきます。

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\View\View;

class PostController extends Controller
{
    /**
     * Show the form to create a new blog post.
     */
    public function create(): View
    {
        return view('post.create');
    }

    /**
     * Store a new blog post.
     */
    public function store(Request $request): RedirectResponse
    {
        // Validate and store the blog post...

        $post = /** ... */

        return to_route('post.show', ['post' => $post->id]);
    }
}
```

<a name="quick-writing-the-validation-logic"></a>
<!-- ### Writing the Validation Logic -->
### Writing the Validation Logic

<!-- Now we are ready to fill in our `store` method with the logic to validate the new blog post. To do this, we will use the `validate` method provided by the `Illuminate\Http\Request` object. If the validation rules pass, your code will keep executing normally; however, if validation fails, an `Illuminate\Validation\ValidationException` exception will be thrown and the proper error response will automatically be sent back to the user. -->
これで、新しいブログ投稿を検証するロジックを `store` メソッドに入力する準備が整いました。これを行うには、`Illuminate\Http\Request` オブジェクトによって提供される `validate` メソッドを使用します。検証ルールに合格すると、コードは通常どおりに実行され続けます。ただし、検証が失敗した場合は、`Illuminate\Validation\ValidationException` 例外がスローされ、適切なエラー応答が自動的にユーザーに返されます。

<!-- If validation fails during a traditional HTTP request, a redirect response to the previous URL will be generated. If the incoming request is an XHR request, a [JSON response containing the validation error messages](#validation-error-response-format) will be returned. -->
従来の HTTP リクエスト中に検証が失敗した場合、前の URL へのリダイレクト応答が生成されます。受信リクエストが XHR リクエストの場合、[JSON response containing the validation error messages](#validation-error-response-format) が返されます。

<!-- To get a better understanding of the `validate` method, let's jump back into the `store` method: -->
`validate` メソッドをより深く理解するために、`store` メソッドに戻りましょう。

```php
/**
 * Store a new blog post.
 */
public function store(Request $request): RedirectResponse
{
    $validated = $request->validate([
        'title' => ['required', 'unique:posts', 'max:255'],
        'body' => ['required'],
    ]);

    // The blog post is valid...

    return redirect('/posts');
}
```

<!-- As you can see, the validation rules are passed into the `validate` method. Don't worry - all available validation rules are [documented](#available-validation-rules). Again, if the validation fails, the proper response will automatically be generated. If the validation passes, our controller will continue executing normally. -->
ご覧のとおり、検証ルールは `validate` メソッドに渡されます。心配しないでください。使用可能な検証ルールはすべて [documented](#available-validation-rules) です。繰り返しますが、検証が失敗した場合は、適切な応答が自動的に生成されます。検証に合格すると、コントローラは通常どおりに実行を続けます。

<!-- In addition, you may use the `validateWithBag` method to validate a request and store any error messages within a [named error bag](#named-error-bags): -->
さらに、`validateWithBag` メソッドを使用してリクエストを検証し、エラー メッセージを [named error bag](#named-error-bags) 内に保存することもできます。

```php
$validated = $request->validateWithBag('post', [
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

<a name="stopping-on-first-validation-failure"></a>
<!-- #### Stopping on First Validation Failure -->
#### Stopping on First Validation Failure

<!-- Sometimes you may wish to stop running validation rules on an attribute after the first validation failure. To do so, assign the `bail` rule to the attribute: -->
最初の検証が失敗した後、属性に対する検証ルールの実行を停止したい場合があります。これを行うには、`bail` ルールを属性に割り当てます。

```php
$request->validate([
    'title' => ['bail', 'required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```

<!-- In this example, if the `unique` rule on the `title` attribute fails, the `max` rule will not be checked. Rules will be validated in the order they are assigned. -->
この例では、`title` 属性の `unique` ルールが失敗した場合、`max` ルールはチェックされません。ルールは割り当てられた順序で検証されます。

<a name="a-note-on-nested-attributes"></a>
<!-- #### A Note on Nested Attributes -->
#### A Note on Nested Attributes

<!-- If the incoming HTTP request contains "nested" field data, you may specify these fields in your validation rules using "dot" syntax: -->
受信した HTTP リクエストに「ネストされた」フィールド データが含まれている場合は、「ドット」構文を使用して検証ルールでこれらのフィールドを指定できます。

```php
$request->validate([
    'title' => ['required', 'unique:posts', 'max:255'],
    'author.name' => ['required'],
    'author.description' => ['required'],
]);
```

<!-- On the other hand, if your field name contains a literal period, you can explicitly prevent this from being interpreted as "dot" syntax by escaping the period with a backslash: -->
一方、フィールド名にリテラルのピリオドが含まれている場合は、ピリオドをバックスラッシュでエスケープすることで、これが「ドット」構文として解釈されるのを明示的に防ぐことができます。

```php
$request->validate([
    'title' => ['required', 'unique:posts', 'max:255'],
    'v1\.0' => ['required'],
]);
```

<a name="quick-displaying-the-validation-errors"></a>
<!-- ### Displaying the Validation Errors -->
### Displaying the Validation Errors

<!-- So, what if the incoming request fields do not pass the given validation rules? As mentioned previously, Laravel will automatically redirect the user back to their previous location. In addition, all of the validation errors and [request input](/docs/13.x/requests#retrieving-old-input) will automatically be [flashed to the session](/docs/13.x/session#flash-data). -->
では、受信リクエストフィールドが指定された検証ルールを通過しない場合はどうなるでしょうか?前述したように、Laravel はユーザーを以前の場所に自動的にリダイレクトします。さらに、すべての検証エラーと [request input](/docs/13.x/requests#retrieving-old-input) は自動的に [flashed to the session](/docs/13.x/session#flash-data) になります。

<!-- An `$errors` variable is shared with all of your application's views by the `Illuminate\View\Middleware\ShareErrorsFromSession` middleware, which is provided by the `web` middleware group. When this middleware is applied an `$errors` variable will always be available in your views, allowing you to conveniently assume the `$errors` variable is always defined and can be safely used. The `$errors` variable will be an instance of `Illuminate\Support\MessageBag`. For more information on working with this object, [check out its documentation](#working-with-error-messages). -->
`$errors` 変数は、`web` ミドルウェア グループによって提供される `Illuminate\View\Middleware\ShareErrorsFromSession` ミドルウェアによって、アプリケーションのすべてのビューと共有されます。このミドルウェアを適用すると、`$errors` 変数が常にビューで使用できるようになり、都合よく、`$errors` 変数が常に定義されており、安全に使用できると想定できます。 `$errors` 変数は、`Illuminate\Support\MessageBag` のインスタンスになります。このオブジェクトの操作の詳細については、[check out its documentation](#working-with-error-messages) を参照してください。

<!-- So, in our example, the user will be redirected to our controller's `create` method when validation fails, allowing us to display the error messages in the view: -->
したがって、この例では、検証が失敗したときにユーザーはコントローラの `create` メソッドにリダイレクトされ、ビューにエラー メッセージを表示できるようになります。

```blade
<!-- /resources/views/post/create.blade.php -->

<h1>Create Post</h1>

@if ($errors->any())
    <div class="alert alert-danger">
        <ul>
            @foreach ($errors->all() as $error)
                <li>{{ $error }}</li>
            @endforeach
        </ul>
    </div>
@endif

<!-- Create Post Form -->
```

<a name="quick-customizing-the-error-messages"></a>
<!-- #### Customizing the Error Messages -->
#### Customizing the Error Messages

<!-- Laravel's built-in validation rules each have an error message that is located in your application's `lang/en/validation.php` file. If your application does not have a `lang` directory, you may instruct Laravel to create it using the `lang:publish` Artisan command. -->
Laravel の組み込み検証ルールには、それぞれエラー メッセージがあり、アプリケーションの `lang/en/validation.php` ファイルにあります。アプリケーションに `lang` ディレクトリがない場合は、`lang:publish` Artisan コマンドを使用してディレクトリを作成するように Laravel に指示できます。

<!-- Within the `lang/en/validation.php` file, you will find a translation entry for each validation rule. You are free to change or modify these messages based on the needs of your application. -->
`lang/en/validation.php` ファイル内に、各検証ルールの変換エントリがあります。アプリケーションのニーズに基づいて、これらのメッセージを自由に変更または修正できます。

<!-- In addition, you may copy this file to another language directory to translate the messages for your application's language. To learn more about Laravel localization, check out the complete [localization documentation](/docs/13.x/localization). -->
さらに、このファイルを別の言語ディレクトリにコピーして、メッセージをアプリケーションの言語に翻訳することもできます。 Laravel ローカリゼーションの詳細については、完全な [localization documentation](/docs/13.x/localization) を確認してください。

> [!WARNING]
> デフォルトでは、Laravel アプリケーションのスケルトンには `lang` ディレクトリが含まれません。 Laravel の言語ファイルをカスタマイズしたい場合は、`lang:publish` Artisan コマンドを使用して言語ファイルを公開できます。

<a name="quick-xhr-requests-and-validation"></a>
<!-- #### XHR Requests and Validation -->
#### XHR Requests and Validation

<!-- In this example, we used a traditional form to send data to the application. However, many applications receive XHR requests from a JavaScript powered frontend. When using the `validate` method during an XHR request, Laravel will not generate a redirect response. Instead, Laravel generates a [JSON response containing all of the validation errors](#validation-error-response-format). This JSON response will be sent with a 422 HTTP status code. -->
この例では、従来のフォームを使用してデータをアプリケーションに送信しました。ただし、多くのアプリケーションは、JavaScript を利用したフロントエンドから XHR リクエストを受け取ります。 XHRリクエスト中に `validate` メソッドを使用すると、Laravelはリダイレクト応答を生成しません。代わりに、Laravel は [JSON response containing all of the validation errors](#validation-error-response-format) を生成します。この JSON 応答は 422 HTTP ステータス コードとともに送信されます。

<a name="the-at-error-directive"></a>
<!-- #### The `@error` Directive -->
#### The `@error` Directive

<!-- You may use the `@error` [Blade](/docs/13.x/blade) directive to quickly determine if validation error messages exist for a given attribute. Within an `@error` directive, you may echo the `$message` variable to display the error message: -->
`@error` [Blade](/docs/13.x/blade) ディレクティブを使用すると、特定の属性に検証エラー メッセージが存在するかどうかを迅速に判断できます。 `@error` ディレクティブ内で、`$message` 変数をエコーし​​てエラー メッセージを表示できます。

```blade
<!-- /resources/views/post/create.blade.php -->

<label for="title">Post Title</label>

<input
    id="title"
    type="text"
    name="title"
    class="@error('title') is-invalid @enderror"
/>

@error('title')
    <div class="alert alert-danger">{{ $message }}</div>
@enderror
```

<!-- If you are using [named error bags](#named-error-bags), you may pass the name of the error bag as the second argument to the `@error` directive: -->
[named error bags](#named-error-bags) を使用している場合は、エラー バッグの名前を 2 番目の引数として `@error` ディレクティブに渡すことができます。

```blade
<input ... class="@error('title', 'post') is-invalid @enderror">
```

<a name="repopulating-forms"></a>
<!-- ### Repopulating Forms -->
### Repopulating Forms

<!-- When Laravel generates a redirect response due to a validation error, the framework will automatically [flash all of the request's input to the session](/docs/13.x/session#flash-data). This is done so that you may conveniently access the input during the next request and repopulate the form that the user attempted to submit. -->
Laravel が検証エラーによりリダイレクト応答を生成すると、フレームワークは自動的に [flash all of the request's input to the session](/docs/13.x/session#flash-data) を実行します。これは、次のリクエスト中に入力に簡単にアクセスし、ユーザーが送信しようとしたフォームに再入力できるようにするために行われます。

<!-- To retrieve flashed input from the previous request, invoke the `old` method on an instance of `Illuminate\Http\Request`. The `old` method will pull the previously flashed input data from the [session](/docs/13.x/session): -->
前のリクエストからフラッシュされた入力を取得するには、`Illuminate\Http\Request` のインスタンスで `old` メソッドを呼び出します。 `old` メソッドは、以前にフラッシュされた入力データを [session](/docs/13.x/session) から取得します。

```php
$title = $request->old('title');
```

<!-- Laravel also provides a global `old` helper. If you are displaying old input within a [Blade template](/docs/13.x/blade), it is more convenient to use the `old` helper to repopulate the form. If no old input exists for the given field, `null` will be returned: -->
Laravel は、グローバル `old` ヘルパも提供します。 [Blade template](/docs/13.x/blade) 内で古い入力を表示している場合は、`old` ヘルパを使用してフォームに再入力する方が便利です。指定されたフィールドに古い入力が存在しない場合は、`null` が返されます。

```blade
<input type="text" name="title" value="{{ old('title') }}">
```

<a name="a-note-on-optional-fields"></a>
<!-- ### A Note on Optional Fields -->
### A Note on Optional Fields

<!-- By default, Laravel includes the `TrimStrings` and `ConvertEmptyStringsToNull` middleware in your application's global middleware stack. Because of this, you will often need to mark your "optional" request fields as `nullable` if you do not want the validator to consider `null` values as invalid. For example: -->
デフォルトでは、Laravel にはアプリケーションのグローバルミドルウェアスタックに `TrimStrings` および `ConvertEmptyStringsToNull` ミドルウェアが含まれています。このため、バリデーターで `null` 値が無効であるとみなされたくない場合は、多くの場合、「オプション」リクエスト フィールドを `nullable` としてマークする必要があります。例えば：

```php
$request->validate([
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
    'publish_at' => ['nullable', 'date'],
]);
```

<!-- In this example, we are specifying that the `publish_at` field may be either `null` or a valid date representation. If the `nullable` modifier is not added to the rule definition, the validator would consider `null` an invalid date. -->
この例では、`publish_at` フィールドが `null` または有効な日付表現のいずれかであることを指定しています。 `nullable` 修飾子がルール定義に追加されていない場合、バリデーターは `null` を無効な日付と見なします。

<a name="validation-error-response-format"></a>
<!-- ### Validation Error Response Format -->
### Validation Error Response Format

<!-- When your application throws a `Illuminate\Validation\ValidationException` exception and the incoming HTTP request is expecting a JSON response, Laravel will automatically format the error messages for you and return a `422 Unprocessable Entity` HTTP response. -->
アプリケーションが `Illuminate\Validation\ValidationException` 例外をスローし、受信 HTTP リクエストが JSON レスポンスを期待している場合、Laravel はエラーメッセージを自動的にフォーマットし、`422 Unprocessable Entity` HTTP レスポンスを返します。

<!-- Below, you can review an example of the JSON response format for validation errors. Note that nested error keys are flattened into "dot" notation format: -->
以下では、検証エラーの JSON 応答形式の例を確認できます。ネストされたエラー キーは「ドット」表記形式に平坦化されることに注意してください。

```json
{
    "message": "The team name must be a string. (and 4 more errors)",
    "errors": {
        "team_name": [
            "The team name must be a string.",
            "The team name must be at least 1 characters."
        ],
        "authorization.role": [
            "The selected authorization.role is invalid."
        ],
        "users.0.email": [
            "The users.0.email field is required."
        ],
        "users.2.email": [
            "The users.2.email must be a valid email address."
        ]
    }
}
```

<a name="form-request-validation"></a>
<!-- ## Form Request Validation -->
## Form Request Validation

<a name="creating-form-requests"></a>
<!-- ### Creating Form Requests -->
### Creating Form Requests

<!-- For more complex validation scenarios, you may wish to create a "form request". Form requests are custom request classes that encapsulate their own validation and authorization logic. To create a form request class, you may use the `make:request` Artisan CLI command: -->
より複雑な検証シナリオの場合は、「フォームリクエスト」を作成することもできます。フォームリクエストは、独自の検証および認可ロジックをカプセル化するカスタムリクエストクラスです。フォームリクエストクラスを作成するには、`make:request` Artisan CLI コマンドを使用できます。

```shell
php artisan make:request StorePostRequest
```

<!-- The generated form request class will be placed in the `app/Http/Requests` directory. If this directory does not exist, it will be created when you run the `make:request` command. Each form request generated by Laravel has two methods: `authorize` and `rules`. -->
生成されたフォーム要求クラスは、`app/Http/Requests` ディレクトリに配置されます。このディレクトリが存在しない場合は、`make:request` コマンドを実行すると作成されます。 Laravel によって生成された各フォームリクエストには、`authorize` と `rules` という 2 つのメソッドがあります。

<!-- As you might have guessed, the `authorize` method is responsible for determining if the currently authenticated user can perform the action represented by the request, while the `rules` method returns the validation rules that should apply to the request's data: -->
ご想像のとおり、`authorize` メソッドは、現在認証されているユーザーがリクエストで表されるアクションを実行できるかどうかを判断する役割を果たし、一方、`rules` メソッドはリクエストのデータに適用する必要がある検証ルールを返します。

```php
/**
 * Get the validation rules that apply to the request.
 *
 * @return array<string, \Illuminate\Contracts\Validation\ValidationRule|array<mixed>|string>
 */
public function rules(): array
{
    return [
        'title' => ['required', 'unique:posts', 'max:255'],
        'body' => ['required'],
    ];
}
```

> [!NOTE]
> `rules` メソッドのシグネチャ内で必要な依存関係をタイプヒントで指定できます。これらは、Laravel [service container](/docs/13.x/container) を通じて自動的に解決されます。

<!-- So, how are the validation rules evaluated? All you need to do is type-hint the request on your controller method. The incoming form request is validated before the controller method is called, meaning you do not need to clutter your controller with any validation logic: -->
では、検証ルールはどのように評価されるのでしょうか?必要なのは、コントローラ メソッドでリクエストをタイプヒントすることだけです。受信したフォームリクエストはコントローラメソッドが呼び出される前に検証されます。つまり、コントローラに検証ロジックを複雑にする必要はありません。

```php
/**
 * Store a new blog post.
 */
public function store(StorePostRequest $request): RedirectResponse
{
    // The incoming request is valid...

    // Retrieve the validated input data...
    $validated = $request->validated();

    // Retrieve a portion of the validated input data...
    $validated = $request->safe()->only(['name', 'email']);
    $validated = $request->safe()->except(['name', 'email']);

    // Store the blog post...

    return redirect('/posts');
}
```

<!-- If validation fails, a redirect response will be generated to send the user back to their previous location. The errors will also be flashed to the session so they are available for display. If the request was an XHR request, an HTTP response with a 422 status code will be returned to the user including a [JSON representation of the validation errors](#validation-error-response-format). -->
検証が失敗した場合は、ユーザーを以前の場所に戻すリダイレクト応答が生成されます。エラーはセッションにもフラッシュされるので、表示できるようになります。リクエストが XHR リクエストの場合、[JSON representation of the validation errors](#validation-error-response-format) を含む 422 ステータス コードを含む HTTP 応答がユーザーに返されます。

> [!NOTE]
> Inertia を利用した Laravel フロントエンドにリアルタイムのフォームリクエスト検証を追加する必要がありますか? [Laravel Precognition](/docs/13.x/precognition) をチェックしてください。

<a name="performing-additional-validation-on-form-requests"></a>
<!-- #### Performing Additional Validation -->
#### Performing Additional Validation

<!-- Sometimes you need to perform additional validation after your initial validation is complete. You can accomplish this using the form request's `after` method. -->
場合によっては、最初の検証が完了した後、追加の検証を実行する必要があります。これは、フォームリクエストの `after` メソッドを使用して実現できます。

<!-- The `after` method should return an array of callables or closures which will be invoked after validation is complete. The given callables will receive an `Illuminate\Validation\Validator` instance, allowing you to raise additional error messages if necessary: -->
`after` メソッドは、検証の完了後に呼び出される呼び出し可能オブジェクトまたはクロージャの配列を返す必要があります。指定された呼び出し可能オブジェクトは `Illuminate\Validation\Validator` インスタンスを受け取り、必要に応じて追加のエラー メッセージを生成できるようになります。

```php
use Illuminate\Validation\Validator;

/**
 * Get the "after" validation callables for the request.
 */
public function after(): array
{
    return [
        function (Validator $validator) {
            if ($this->somethingElseIsInvalid()) {
                $validator->errors()->add(
                    'field',
                    'Something is wrong with this field!'
                );
            }
        }
    ];
}
```

<!-- As noted, the array returned by the `after` method may also contain invokable classes. The `__invoke` method of these classes will receive an `Illuminate\Validation\Validator` instance: -->
前述したように、`after` メソッドによって返される配列には、呼び出し可能なクラスも含まれる場合があります。これらのクラスの `__invoke` メソッドは、`Illuminate\Validation\Validator` インスタンスを受け取ります。

```php
use App\Validation\ValidateShippingTime;
use App\Validation\ValidateUserStatus;
use Illuminate\Validation\Validator;

/**
 * Get the "after" validation callables for the request.
 */
public function after(): array
{
    return [
        new ValidateUserStatus,
        new ValidateShippingTime,
        function (Validator $validator) {
            //
        }
    ];
}
```

<a name="request-stopping-on-first-validation-rule-failure"></a>
<!-- #### Stopping on the First Validation Failure -->
#### Stopping on the First Validation Failure

<!-- By adding the `StopOnFirstFailure` attribute to your request class, you may inform the validator that it should stop validating all attributes once a single validation failure has occurred: -->
リクエスト クラスに `StopOnFirstFailure` 属性を追加することで、検証エラーが 1 回発生したらすべての属性の検証を停止するようバリデーターに通知できます。

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\Attributes\StopOnFirstFailure;
use Illuminate\Foundation\Http\FormRequest;

#[StopOnFirstFailure]
class StorePostRequest extends FormRequest
{
    // ...
}
```

<a name="request-failing-on-unknown-fields"></a>
<!-- #### Failing on Unknown Fields -->
#### Failing on Unknown Fields

<!-- By adding the `FailOnUnknownFields` attribute to your request class, you may instruct Laravel to reject any incoming fields that are not defined by your request's validation rules: -->
リクエストクラスに `FailOnUnknownFields` 属性を追加することで、リクエストの検証ルールで定義されていない受信フィールドを拒否するように Laravel に指示できます。

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\Attributes\FailOnUnknownFields;
use Illuminate\Foundation\Http\FormRequest;

#[FailOnUnknownFields]
class StorePostRequest extends FormRequest
{
    public function rules(): array
    {
        return [
            'title' => ['required', 'string'],
            'body' => ['required', 'string'],
        ];
    }
}
```

<!-- You may also enable this behavior globally for all form requests from your `AppServiceProvider`: -->
`AppServiceProvider` からのすべてのフォームリクエストに対してこの動作をグローバルに有効にすることもできます。

```php
use Illuminate\Foundation\Http\FormRequest;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    FormRequest::failOnUnknownFields();
}
```

<!-- If needed, you may disable this behavior for a specific request by passing `false` to the attribute: -->
必要に応じて、`false` を属性に渡すことで、特定のリクエストに対してこの動作を無効にすることができます。

```php
#[FailOnUnknownFields(false)]
class PublicWebhookRequest extends FormRequest
{
    // ...
}
```

<!-- Rejecting unknown fields can provide additional protection against mass-assignment style issues by preventing unexpected input keys from flowing deeper into your application. However, you should still configure your model's `$fillable` / `$guarded` properties and only persist trusted, validated input. -->
不明なフィールドを拒否すると、予期しない入力キーがアプリケーションの奥深くに流入するのを防ぐことで、一括代入スタイルの問題に対する追加の保護を提供できます。ただし、モデルの `$fillable` / `$guarded` プロパティを構成し、信頼できる検証済みの入力のみを保持する必要があります。

<a name="customizing-the-redirect-location"></a>
<!-- #### Customizing the Redirect Location -->
#### Customizing the Redirect Location

<!-- When form request validation fails, a redirect response will be generated to send the user back to their previous location. However, you are free to customize this behavior. To do so, you may use the `RedirectTo` attribute on your form request: -->
フォームリクエストの検証が失敗すると、ユーザーを以前の場所に戻すリダイレクト応答が生成されます。ただし、この動作は自由にカスタマイズできます。これを行うには、フォームリクエストで `RedirectTo` 属性を使用します。

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\Attributes\RedirectTo;
use Illuminate\Foundation\Http\FormRequest;

#[RedirectTo('/dashboard')]
class StorePostRequest extends FormRequest
{
    // ...
}
```

<!-- Or, if you would like to redirect users to a named route, you may use the `RedirectToRoute` attribute instead: -->
または、ユーザーを名前付きルートにリダイレクトしたい場合は、代わりに `RedirectToRoute` 属性を使用できます。

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\Attributes\RedirectToRoute;
use Illuminate\Foundation\Http\FormRequest;

#[RedirectToRoute('dashboard')]
class StorePostRequest extends FormRequest
{
    // ...
}
```

<a name="customizing-the-error-bag"></a>
<!-- #### Customizing the Error Bag -->
#### Customizing the Error Bag

<!-- When form request validation fails, the errors are flashed to the `default` error bag. If you need to store the errors in a different [named error bag](#named-error-bags), you may use the `ErrorBag` attribute on your form request: -->
フォームリクエストの検証が失敗すると、エラーは `default` エラー バッグにフラッシュされます。エラーを別の [named error bag](#named-error-bags) に保存する必要がある場合は、フォーム リクエストで `ErrorBag` 属性を使用できます。

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\Attributes\ErrorBag;
use Illuminate\Foundation\Http\FormRequest;

#[ErrorBag('login')]
class LoginRequest extends FormRequest
{
    // ...
}
```

<a name="authorizing-form-requests"></a>
<!-- ### Authorizing Form Requests -->
### Authorizing Form Requests

<!-- The form request class also contains an `authorize` method. Within this method, you may determine if the authenticated user actually has the authority to update a given resource. For example, you may determine if a user actually owns a blog comment they are attempting to update. Most likely, you will interact with your [authorization gates and policies](/docs/13.x/authorization) within this method: -->
フォーム要求クラスには、`authorize` メソッドも含まれています。このメソッド内で、認証されたユーザーが実際に特定のリソースを更新する権限を持っているかどうかを判断できます。たとえば、ユーザーが更新しようとしているブログ コメントを実際に所有しているかどうかを判断できます。おそらく、次のメソッド内で [authorization gates and policies](/docs/13.x/authorization) を操作することになります。

```php
use App\Models\Comment;

/**
 * Determine if the user is authorized to make this request.
 */
public function authorize(): bool
{
    $comment = Comment::find($this->route('comment'));

    return $comment && $this->user()->can('update', $comment);
}
```

<!-- Since all form requests extend the base Laravel request class, we may use the `user` method to access the currently authenticated user. Also, note the call to the `route` method in the example above. This method grants you access to the URI parameters defined on the route being called, such as the `{comment}` parameter in the example below: -->
すべてのフォームリクエストは基本Laravelリクエストクラスを拡張するため、`user` メソッドを使用して現在認証されているユーザーにアクセスできます。また、上記の例の `route` メソッドの呼び出しにも注意してください。このメソッドを使用すると、以下の例の `{comment}` パラメーターなど、呼び出されるルートで定義された URI パラメーターへのアクセスが許可されます。

```php
Route::post('/comment/{comment}');
```

<!-- Therefore, if your application is taking advantage of [route model binding](/docs/13.x/routing#route-model-binding), your code may be made even more succinct by accessing the resolved model as a property of the request: -->
したがって、アプリケーションが [route model binding](/docs/13.x/routing#route-model-binding) を利用している場合は、リクエストのプロパティとして解決されたモデルにアクセスすることで、コードをさらに簡潔にすることができます。

```php
return $this->user()->can('update', $this->comment);
```

<!-- If the `authorize` method returns `false`, an HTTP response with a 403 status code will automatically be returned and your controller method will not execute. -->
`authorize` メソッドが `false` を返した場合、403 ステータス コードを含む HTTP 応答が自動的に返され、コントローラ メソッドは実行されません。

<!-- If you plan to handle authorization logic for the request in another part of your application, you may remove the `authorize` method completely, or simply return `true`: -->
アプリケーションの別の部分でリクエストの認可ロジックを処理する予定がある場合は、`authorize` メソッドを完全に削除するか、単純に `true` を返すことができます。

```php
/**
 * Determine if the user is authorized to make this request.
 */
public function authorize(): bool
{
    return true;
}
```

> [!NOTE]
> `authorize` メソッドのシグネチャ内で必要な依存関係をタイプヒントで指定できます。これらは、Laravel [service container](/docs/13.x/container) を通じて自動的に解決されます。

<a name="customizing-the-error-messages"></a>
<!-- ### Customizing the Error Messages -->
### Customizing the Error Messages

<!-- You may customize the error messages used by the form request by overriding the `messages` method. This method should return an array of attribute / rule pairs and their corresponding error messages: -->
`messages` メソッドをオーバーライドすることで、フォーム リクエストで使用されるエラー メッセージをカスタマイズできます。このメソッドは、属性とルールのペアの配列と、それに対応するエラー メッセージを返す必要があります。

```php
/**
 * Get the error messages for the defined validation rules.
 *
 * @return array<string, string>
 */
public function messages(): array
{
    return [
        'title.required' => 'A title is required',
        'body.required' => 'A message is required',
    ];
}
```

<a name="customizing-the-validation-attributes"></a>
<!-- #### Customizing the Validation Attributes -->
#### Customizing the Validation Attributes

<!-- Many of Laravel's built-in validation rule error messages contain an `:attribute` placeholder. If you would like the `:attribute` placeholder of your validation message to be replaced with a custom attribute name, you may specify the custom names by overriding the `attributes` method. This method should return an array of attribute / name pairs: -->
Laravel の組み込み検証ルールのエラー メッセージの多くには、`:attribute` プレースホルダーが含まれています。検証メッセージの `:attribute` プレースホルダーをカスタム属性名に置き換えたい場合は、`attributes` メソッドをオーバーライドしてカスタム名を指定できます。このメソッドは、属性と名前のペアの配列を返す必要があります。

```php
/**
 * Get custom attributes for validator errors.
 *
 * @return array<string, string>
 */
public function attributes(): array
{
    return [
        'email' => 'email address',
    ];
}
```

<a name="preparing-input-for-validation"></a>
<!-- ### Preparing Input for Validation -->
### Preparing Input for Validation

<!-- If you need to prepare or sanitize any data from the request before you apply your validation rules, you may use the `prepareForValidation` method: -->
検証ルールを適用する前にリクエストのデータを準備またはサニタイズする必要がある場合は、`prepareForValidation` メソッドを使用できます。

```php
use Illuminate\Support\Str;

/**
 * Prepare the data for validation.
 */
protected function prepareForValidation(): void
{
    $this->merge([
        'slug' => Str::slug($this->slug),
    ]);
}
```

<!-- Likewise, if you need to normalize any request data after validation is complete, you may use the `passedValidation` method: -->
同様に、検証の完了後にリクエスト データを正規化する必要がある場合は、`passedValidation` メソッドを使用できます。

```php
/**
 * Handle a passed validation attempt.
 */
protected function passedValidation(): void
{
    $this->replace(['name' => 'Taylor']);
}
```

<a name="manually-creating-validators"></a>
<!-- ## Manually Creating Validators -->
## Manually Creating Validators

<!-- If you do not want to use the `validate` method on the request, you may create a validator instance manually using the `Validator` [facade](/docs/13.x/facades). The `make` method on the facade generates a new validator instance: -->
リクエストで `validate` メソッドを使用したくない場合は、`Validator` [facade](/docs/13.x/facades) を使用してバリデーター インスタンスを手動で作成できます。ファサードの `make` メソッドは、新しいバリデーター インスタンスを生成します。

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;

class PostController extends Controller
{
    /**
     * Store a new blog post.
     */
    public function store(Request $request): RedirectResponse
    {
        $validator = Validator::make($request->all(), [
            'title' => ['required', 'unique:posts', 'max:255'],
            'body' => ['required'],
        ]);

        if ($validator->fails()) {
            return redirect('/post/create')
                ->withErrors($validator)
                ->withInput();
        }

        // Retrieve the validated input...
        $validated = $validator->validated();

        // Retrieve a portion of the validated input...
        $validated = $validator->safe()->only(['name', 'email']);
        $validated = $validator->safe()->except(['name', 'email']);

        // Store the blog post...

        return redirect('/posts');
    }
}
```

<!-- The first argument passed to the `make` method is the data under validation. The second argument is an array of the validation rules that should be applied to the data. -->
`make` メソッドに渡される最初の引数は、検証対象のデータです。 2 番目の引数は、データに適用する必要がある検証ルールの配列です。

<!-- After determining whether the request validation failed, you may use the `withErrors` method to flash the error messages to the session. When using this method, the `$errors` variable will automatically be shared with your views after redirection, allowing you to easily display them back to the user. The `withErrors` method accepts a validator, a `MessageBag`, or a PHP `array`. -->
リクエストの検証が失敗したかどうかを確認した後、`withErrors` メソッドを使用してエラー メッセージをセッションにフラッシュできます。この方法を使用すると、リダイレクト後に `$errors` 変数がビューと自動的に共有されるため、ビューを簡単にユーザーに表示できるようになります。 `withErrors` メソッドは、バリデータ、`MessageBag`、または PHP `array` を受け入れます。

<!-- #### Stopping on First Validation Failure -->
#### Stopping on First Validation Failure

<!-- The `stopOnFirstFailure` method will inform the validator that it should stop validating all attributes once a single validation failure has occurred: -->
`stopOnFirstFailure` メソッドは、検証エラーが 1 回発生すると、すべての属性の検証を停止する必要があることをバリデーターに通知します。

```php
if ($validator->stopOnFirstFailure()->fails()) {
    // ...
}
```

<a name="automatic-redirection"></a>
<!-- ### Automatic Redirection -->
### Automatic Redirection

<!-- If you would like to create a validator instance manually but still take advantage of the automatic redirection offered by the HTTP request's `validate` method, you may call the `validate` method on an existing validator instance. If validation fails, the user will automatically be redirected or, in the case of an XHR request, a [JSON response will be returned](#validation-error-response-format): -->
バリデーター インスタンスを手動で作成したいが、HTTP リクエストの `validate` メソッドによって提供される自動リダイレクトを利用したい場合は、既存のバリデーター インスタンスで `validate` メソッドを呼び出すことができます。検証が失敗した場合、ユーザーは自動的にリダイレクトされるか、XHR リクエストの場合は [JSON response will be returned](#validation-error-response-format) にリダイレクトされます。

```php
Validator::make($request->all(), [
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
])->validate();
```

<!-- You may use the `validateWithBag` method to store the error messages in a [named error bag](#named-error-bags) if validation fails: -->
検証が失敗した場合は、`validateWithBag` メソッドを使用してエラー メッセージを [named error bag](#named-error-bags) に保存できます。

```php
Validator::make($request->all(), [
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
])->validateWithBag('post');
```

<a name="named-error-bags"></a>
<!-- ### Named Error Bags -->
### Named Error Bags

<!-- If you have multiple forms on a single page, you may wish to name the `MessageBag` containing the validation errors, allowing you to retrieve the error messages for a specific form. To achieve this, pass a name as the second argument to `withErrors`: -->
1 つのページに複数のフォームがある場合は、検証エラーを含む `MessageBag` に名前を付けると、特定のフォームのエラー メッセージを取得できるようになります。これを実現するには、2 番目の引数として名前を `withErrors` に渡します。

```php
return redirect('/register')->withErrors($validator, 'login');
```

<!-- You may then access the named `MessageBag` instance from the `$errors` variable: -->
その後、`$errors` 変数から名前付き `MessageBag` インスタンスにアクセスできます。

```blade
{{ $errors->login->first('email') }}
```

<a name="manual-customizing-the-error-messages"></a>
<!-- ### Customizing the Error Messages -->
### Customizing the Error Messages

<!-- If needed, you may provide custom error messages that a validator instance should use instead of the default error messages provided by Laravel. There are several ways to specify custom messages. First, you may pass the custom messages as the third argument to the `Validator::make` method: -->
必要に応じて、Laravel が提供するデフォルトのエラーメッセージの代わりに、バリデーターインスタンスが使用するカスタムエラーメッセージを提供できます。カスタム メッセージを指定するにはいくつかの方法があります。まず、カスタム メッセージを `Validator::make` メソッドの 3 番目の引数として渡すことができます。

```php
$validator = Validator::make($input, $rules, $messages = [
    'required' => 'The :attribute field is required.',
]);
```

<!-- In this example, the `:attribute` placeholder will be replaced by the actual name of the field under validation. You may also utilize other placeholders in validation messages. For example: -->
この例では、`:attribute` プレースホルダーは、検証中のフィールドの実際の名前に置き換えられます。検証メッセージで他のプレースホルダーを利用することもできます。例えば：

```php
$messages = [
    'same' => 'The :attribute and :other must match.',
    'size' => 'The :attribute must be exactly :size.',
    'between' => 'The :attribute value :input is not between :min - :max.',
    'in' => 'The :attribute must be one of the following types: :values',
];
```

<a name="specifying-a-custom-message-for-a-given-attribute"></a>
<!-- #### Specifying a Custom Message for a Given Attribute -->
#### Specifying a Custom Message for a Given Attribute

<!-- Sometimes you may wish to specify a custom error message only for a specific attribute. You may do so using "dot" notation. Specify the attribute's name first, followed by the rule: -->
場合によっては、特定の属性に対してのみカスタム エラー メッセージを指定したい場合があります。 「ドット」表記を使用してこれを行うことができます。最初に属性の名前を指定し、次にルールを指定します。

```php
$messages = [
    'email.required' => 'We need to know your email address!',
];
```

<a name="specifying-custom-attribute-values"></a>
<!-- #### Specifying Custom Attribute Values -->
#### Specifying Custom Attribute Values

<!-- Many of Laravel's built-in error messages include an `:attribute` placeholder that is replaced with the name of the field or attribute under validation. To customize the values used to replace these placeholders for specific fields, you may pass an array of custom attributes as the fourth argument to the `Validator::make` method: -->
Laravel の組み込みエラー メッセージの多くには、検証中のフィールドまたは属性の名前に置き換えられる `:attribute` プレースホルダーが含まれています。特定のフィールドのこれらのプレースホルダーを置換するために使用される値をカスタマイズするには、カスタム属性の配列を `Validator::make` メソッドの 4 番目の引数として渡すことができます。

```php
$validator = Validator::make($input, $rules, $messages, [
    'email' => 'email address',
]);
```

<a name="performing-additional-validation"></a>
<!-- ### Performing Additional Validation -->
### Performing Additional Validation

<!-- Sometimes you need to perform additional validation after your initial validation is complete. You can accomplish this using the validator's `after` method. The `after` method accepts a closure or an array of callables which will be invoked after validation is complete. The given callables will receive an `Illuminate\Validation\Validator` instance, allowing you to raise additional error messages if necessary: -->
場合によっては、最初の検証が完了した後、追加の検証を実行する必要があります。これは、バリデーターの `after` メソッドを使用して実現できます。 `after` メソッドは、検証の完了後に呼び出されるクロージャまたは呼び出し可能オブジェクトの配列を受け入れます。指定された呼び出し可能オブジェクトは `Illuminate\Validation\Validator` インスタンスを受け取り、必要に応じて追加のエラー メッセージを生成できるようになります。

```php
use Illuminate\Support\Facades\Validator;

$validator = Validator::make(/* ... */);

$validator->after(function ($validator) {
    if ($this->somethingElseIsInvalid()) {
        $validator->errors()->add(
            'field', 'Something is wrong with this field!'
        );
    }
});

if ($validator->fails()) {
    // ...
}
```

<!-- As noted, the `after` method also accepts an array of callables, which is particularly convenient if your "after validation" logic is encapsulated in invokable classes, which will receive an `Illuminate\Validation\Validator` instance via their `__invoke` method: -->
前述したように、`after` メソッドは呼び出し可能な配列も受け入れます。これは、「検証後」ロジックが呼び出し可能なクラスにカプセル化されている場合に特に便利です。呼び出し可能なクラスは、`__invoke` メソッドを介して `Illuminate\Validation\Validator` インスタンスを受け取ります。

```php
use App\Validation\ValidateShippingTime;
use App\Validation\ValidateUserStatus;

$validator->after([
    new ValidateUserStatus,
    new ValidateShippingTime,
    function ($validator) {
        // ...
    },
]);
```

<a name="working-with-validated-input"></a>
<!-- ## Working With Validated Input -->
## Working With Validated Input

<!-- After validating incoming request data using a form request or a manually created validator instance, you may wish to retrieve the incoming request data that actually underwent validation. This can be accomplished in several ways. First, you may call the `validated` method on a form request or validator instance. This method returns an array of the data that was validated: -->
フォームリクエストまたは手動で作成したバリデータインスタンスを使用して受信リクエストデータを検証した後、実際に検証を受けた受信リクエストデータを取得したい場合があります。これはいくつかの方法で実現できます。まず、フォームリクエストまたはバリデーターインスタンスで `validated` メソッドを呼び出すことができます。このメソッドは、検証されたデータの配列を返します。

```php
$validated = $request->validated();

$validated = $validator->validated();
```

<!-- Alternatively, you may call the `safe` method on a form request or validator instance. This method returns an instance of `Illuminate\Support\ValidatedInput`. This object exposes `only`, `except`, and `all` methods to retrieve a subset of the validated data or the entire array of validated data: -->
あるいは、フォームリクエストまたはバリデーターインスタンスで `safe` メソッドを呼び出すこともできます。このメソッドは、`Illuminate\Support\ValidatedInput` のインスタンスを返します。このオブジェクトは、検証済みデータのサブセットまたは検証済みデータの配列全体を取得するための `only`、`except`、および `all` メソッドを公開します。

```php
$validated = $request->safe()->only(['name', 'email']);

$validated = $request->safe()->except(['name', 'email']);

$validated = $request->safe()->all();
```

<!-- In addition, the `Illuminate\Support\ValidatedInput` instance may be iterated over and accessed like an array: -->
さらに、`Illuminate\Support\ValidatedInput` インスタンスは配列のように反復され、アクセスされる場合があります。

```php
// Validated data may be iterated...
foreach ($request->safe() as $key => $value) {
    // ...
}

// Validated data may be accessed as an array...
$validated = $request->safe();

$email = $validated['email'];
```

<!-- If you would like to add additional fields to the validated data, you may call the `merge` method: -->
検証されたデータにフィールドを追加したい場合は、`merge` メソッドを呼び出します。

```php
$validated = $request->safe()->merge(['name' => 'Taylor Otwell']);
```

<!-- If you would like to retrieve the validated data as a [collection](/docs/13.x/collections) instance, you may call the `collect` method: -->
検証されたデータを [collection](/docs/13.x/collections) インスタンスとして取得したい場合は、`collect` メソッドを呼び出します。

```php
$collection = $request->safe()->collect();
```

<a name="working-with-error-messages"></a>
<!-- ## Working With Error Messages -->
## Working With Error Messages

<!-- After calling the `errors` method on a `Validator` instance, you will receive an `Illuminate\Support\MessageBag` instance, which has a variety of convenient methods for working with error messages. The `$errors` variable that is automatically made available to all views is also an instance of the `MessageBag` class. -->
`Validator` インスタンスで `errors` メソッドを呼び出した後、エラー メッセージを処理するためのさまざまな便利なメソッドを備えた `Illuminate\Support\MessageBag` インスタンスを受け取ります。すべてのビューで自動的に使用可能になる `$errors` 変数も、`MessageBag` クラスのインスタンスです。

<a name="retrieving-the-first-error-message-for-a-field"></a>
<!-- #### Retrieving the First Error Message for a Field -->
#### Retrieving the First Error Message for a Field

<!-- To retrieve the first error message for a given field, use the `first` method: -->
特定のフィールドの最初のエラー メッセージを取得するには、`first` メソッドを使用します。

```php
$errors = $validator->errors();

echo $errors->first('email');
```

<a name="retrieving-all-error-messages-for-a-field"></a>
<!-- #### Retrieving All Error Messages for a Field -->
#### Retrieving All Error Messages for a Field

<!-- If you need to retrieve an array of all the messages for a given field, use the `get` method: -->
特定のフィールドのすべてのメッセージの配列を取得する必要がある場合は、`get` メソッドを使用します。

```php
foreach ($errors->get('email') as $message) {
    // ...
}
```

<!-- If you are validating an array form field, you may retrieve all of the messages for each of the array elements using the `*` character: -->
配列フォーム フィールドを検証している場合は、`*` 文字を使用して、各配列要素のすべてのメッセージを取得できます。

```php
foreach ($errors->get('attachments.*') as $message) {
    // ...
}
```

<a name="retrieving-all-error-messages-for-all-fields"></a>
<!-- #### Retrieving All Error Messages for All Fields -->
#### Retrieving All Error Messages for All Fields

<!-- To retrieve an array of all messages for all fields, use the `all` method: -->
すべてのフィールドのすべてのメッセージの配列を取得するには、`all` メソッドを使用します。

```php
foreach ($errors->all() as $message) {
    // ...
}
```

<a name="determining-if-messages-exist-for-a-field"></a>
<!-- #### Determining if Messages Exist for a Field -->
#### Determining if Messages Exist for a Field

<!-- The `has` method may be used to determine if any error messages exist for a given field: -->
`has` メソッドは、特定のフィールドにエラー メッセージが存在するかどうかを判断するために使用できます。

```php
if ($errors->has('email')) {
    // ...
}
```

<a name="specifying-custom-messages-in-language-files"></a>
<!-- ### Specifying Custom Messages in Language Files -->
### Specifying Custom Messages in Language Files

<!-- Laravel's built-in validation rules each have an error message that is located in your application's `lang/en/validation.php` file. If your application does not have a `lang` directory, you may instruct Laravel to create it using the `lang:publish` Artisan command. -->
Laravel の組み込み検証ルールには、それぞれエラー メッセージがあり、アプリケーションの `lang/en/validation.php` ファイルにあります。アプリケーションに `lang` ディレクトリがない場合は、`lang:publish` Artisan コマンドを使用してディレクトリを作成するように Laravel に指示できます。

<!-- Within the `lang/en/validation.php` file, you will find a translation entry for each validation rule. You are free to change or modify these messages based on the needs of your application. -->
`lang/en/validation.php` ファイル内に、各検証ルールの変換エントリがあります。アプリケーションのニーズに基づいて、これらのメッセージを自由に変更または修正できます。

<!-- In addition, you may copy this file to another language directory to translate the messages for your application's language. To learn more about Laravel localization, check out the complete [localization documentation](/docs/13.x/localization). -->
さらに、このファイルを別の言語ディレクトリにコピーして、メッセージをアプリケーションの言語に翻訳することもできます。 Laravel ローカリゼーションの詳細については、完全な [localization documentation](/docs/13.x/localization) を確認してください。

> [!WARNING]
> デフォルトでは、Laravel アプリケーションのスケルトンには `lang` ディレクトリが含まれません。 Laravel の言語ファイルをカスタマイズしたい場合は、`lang:publish` Artisan コマンドを使用して言語ファイルを公開できます。

<a name="custom-messages-for-specific-attributes"></a>
<!-- #### Custom Messages for Specific Attributes -->
#### Custom Messages for Specific Attributes

<!-- You may customize the error messages used for specified attribute and rule combinations within your application's validation language files. To do so, add your message customizations to the `custom` array of your application's `lang/xx/validation.php` language file: -->
アプリケーションの検証言語ファイル内の指定された属性とルールの組み合わせに使用されるエラー メッセージをカスタマイズできます。これを行うには、アプリケーションの `lang/xx/validation.php` 言語ファイルの `custom` 配列にメッセージのカスタマイズを追加します。

```php
'custom' => [
    'email' => [
        'required' => 'We need to know your email address!',
        'max' => 'Your email address is too long!'
    ],
],
```

<a name="specifying-attribute-in-language-files"></a>
<!-- ### Specifying Attributes in Language Files -->
### Specifying Attributes in Language Files

<!-- Many of Laravel's built-in error messages include an `:attribute` placeholder that is replaced with the name of the field or attribute under validation. If you would like the `:attribute` portion of your validation message to be replaced with a custom value, you may specify the custom attribute name in the `attributes` array of your `lang/xx/validation.php` language file: -->
Laravel の組み込みエラー メッセージの多くには、検証中のフィールドまたは属性の名前に置き換えられる `:attribute` プレースホルダーが含まれています。検証メッセージの `:attribute` 部分をカスタム値に置き換えたい場合は、`lang/xx/validation.php` 言語ファイルの `attributes` 配列でカスタム属性名を指定できます。

```php
'attributes' => [
    'email' => 'email address',
],
```

> [!WARNING]
> デフォルトでは、Laravel アプリケーションのスケルトンには `lang` ディレクトリが含まれません。 Laravel の言語ファイルをカスタマイズしたい場合は、`lang:publish` Artisan コマンドを使用して言語ファイルを公開できます。

<a name="specifying-values-in-language-files"></a>
<!-- ### Specifying Values in Language Files -->
### Specifying Values in Language Files

<!-- Some of Laravel's built-in validation rule error messages contain a `:value` placeholder that is replaced with the current value of the request attribute. However, you may occasionally need the `:value` portion of your validation message to be replaced with a custom representation of the value. For example, consider the following rule that specifies that a credit card number is required if the `payment_type` has a value of `cc`: -->
Laravel の組み込み検証ルールのエラー メッセージの一部には、リクエスト属性の現在の値に置き換えられる `:value` プレースホルダーが含まれています。ただし、検証メッセージの `:value` 部分を値のカスタム表現に置き換える必要がある場合があります。たとえば、`payment_type` の値が `cc` である場合にクレジット カード番号が必要であることを指定する次のルールを考えてみましょう。

```php
Validator::make($request->all(), [
    'credit_card_number' => ['required_if:payment_type,cc']
]);
```

<!-- If this validation rule fails, it will produce the following error message: -->
この検証ルールが失敗すると、次のエラー メッセージが生成されます。

```text
The credit card number field is required when payment type is cc.
```

<!-- Instead of displaying `cc` as the payment type value, you may specify a more user-friendly value representation in your `lang/xx/validation.php` language file by defining a `values` array: -->
支払いタイプの値として `cc` を表示する代わりに、`values` 配列を定義することで、`lang/xx/validation.php` 言語ファイルでよりユーザーフレンドリーな値表現を指定できます。

```php
'values' => [
    'payment_type' => [
        'cc' => 'credit card'
    ],
],
```

> [!WARNING]
> デフォルトでは、Laravel アプリケーションのスケルトンには `lang` ディレクトリが含まれません。 Laravel の言語ファイルをカスタマイズしたい場合は、`lang:publish` Artisan コマンドを使用して言語ファイルを公開できます。

<!-- After defining this value, the validation rule will produce the following error message: -->
この値を定義すると、検証ルールによって次のエラー メッセージが生成されます。

```text
The credit card number field is required when payment type is credit card.
```

<a name="available-validation-rules"></a>
<!-- ## Available Validation Rules -->
## Available Validation Rules

<!-- Below is a list of all available validation rules and their function: -->
以下は、利用可能なすべての検証ルールとその機能のリストです。

<!-- #### Booleans -->
#### Booleans

<div class="collection-method-list" markdown="1">

<!-- [Accepted](#rule-accepted) [Accepted If](#rule-accepted-if) [Boolean](#rule-boolean) [Declined](#rule-declined) [Declined If](#rule-declined-if) -->
[Accepted](#rule-accepted)
[Accepted If](#rule-accepted-if)
[Boolean](#rule-boolean)
[Declined](#rule-declined)
[Declined If](#rule-declined-if)

</div>

<!-- #### Strings -->
#### Strings

<div class="collection-method-list" markdown="1">

<!-- [Active URL](#rule-active-url) [Alpha](#rule-alpha) [Alpha Dash](#rule-alpha-dash) [Alpha Numeric](#rule-alpha-num) [Ascii](#rule-ascii) [Confirmed](#rule-confirmed) [Current Password](#rule-current-password) [Different](#rule-different) [Doesnt Start With](#rule-doesnt-start-with) [Doesnt End With](#rule-doesnt-end-with) [Email](#rule-email) [Ends With](#rule-ends-with) [Enum](#rule-enum) [Hex Color](#rule-hex-color) [In](#rule-in) [IP Address](#rule-ip) [JSON](#rule-json) [Lowercase](#rule-lowercase) [MAC Address](#rule-mac) [Max](#rule-max) [Min](#rule-min) [Not In](#rule-not-in) [Regular Expression](#rule-regex) [Not Regular Expression](#rule-not-regex) [Same](#rule-same) [Size](#rule-size) [Starts With](#rule-starts-with) [String](#rule-string) [Uppercase](#rule-uppercase) [URL](#rule-url) [ULID](#rule-ulid) [UUID](#rule-uuid) -->
[Active URL](#rule-active-url)
[Alpha](#rule-alpha)
[Alpha Dash](#rule-alpha-dash)
[Alpha Numeric](#rule-alpha-num)
[Ascii](#rule-ascii)
[Confirmed](#rule-confirmed)
[Current Password](#rule-current-password)
[Different](#rule-different)
[Doesnt Start With](#rule-doesnt-start-with)
[Doesnt End With](#rule-doesnt-end-with)
[Email](#rule-email)
[Ends With](#rule-ends-with)
[Enum](#rule-enum)
[Hex Color](#rule-hex-color)
[In](#rule-in)
[IP Address](#rule-ip)
[JSON](#rule-json)
[Lowercase](#rule-lowercase)
[MAC Address](#rule-mac)
[Max](#rule-max)
[Min](#rule-min)
[Not In](#rule-not-in)
[Regular Expression](#rule-regex)
[Not Regular Expression](#rule-not-regex)
[Same](#rule-same)
[Size](#rule-size)
[Starts With](#rule-starts-with)
[String](#rule-string)
[Uppercase](#rule-uppercase)
[URL](#rule-url)
[ULID](#rule-ulid)
[UUID](#rule-uuid)

</div>

<!-- #### Numbers -->
#### Numbers

<div class="collection-method-list" markdown="1">

<!-- [Between](#rule-between) [Decimal](#rule-decimal) [Different](#rule-different) [Digits](#rule-digits) [Digits Between](#rule-digits-between) [Greater Than](#rule-gt) [Greater Than Or Equal](#rule-gte) [Integer](#rule-integer) [Less Than](#rule-lt) [Less Than Or Equal](#rule-lte) [Max](#rule-max) [Max Digits](#rule-max-digits) [Min](#rule-min) [Min Digits](#rule-min-digits) [Multiple Of](#rule-multiple-of) [Numeric](#rule-numeric) [Same](#rule-same) [Size](#rule-size) -->
[Between](#rule-between)
[Decimal](#rule-decimal)
[Different](#rule-different)
[Digits](#rule-digits)
[Digits Between](#rule-digits-between)
[Greater Than](#rule-gt)
[Greater Than Or Equal](#rule-gte)
[Integer](#rule-integer)
[Less Than](#rule-lt)
[Less Than Or Equal](#rule-lte)
[Max](#rule-max)
[Max Digits](#rule-max-digits)
[Min](#rule-min)
[Min Digits](#rule-min-digits)
[Multiple Of](#rule-multiple-of)
[Numeric](#rule-numeric)
[Same](#rule-same)
[Size](#rule-size)

</div>

<!-- #### Arrays -->
#### Arrays

<div class="collection-method-list" markdown="1">

<!-- [Array](#rule-array) [Array Keys](#rule-array-keys) [Between](#rule-between) [Contains](#rule-contains) [Doesnt Contain](#rule-doesnt-contain) [Distinct](#rule-distinct) [In Array](#rule-in-array) [In Array Keys](#rule-in-array-keys) [List](#rule-list) [Max](#rule-max) [Min](#rule-min) [Size](#rule-size) -->
[Array](#rule-array)
[Array Keys](#rule-array-keys)
[Between](#rule-between)
[Contains](#rule-contains)
[Doesnt Contain](#rule-doesnt-contain)
[Distinct](#rule-distinct)
[In Array](#rule-in-array)
[In Array Keys](#rule-in-array-keys)
[List](#rule-list)
[Max](#rule-max)
[Min](#rule-min)
[Size](#rule-size)

</div>

<!-- #### Dates -->
#### Dates

<div class="collection-method-list" markdown="1">

<!-- [After](#rule-after) [After Or Equal](#rule-after-or-equal) [Before](#rule-before) [Before Or Equal](#rule-before-or-equal) [Date](#rule-date) [Date Equals](#rule-date-equals) [Date Format](#rule-date-format) [Different](#rule-different) [Timezone](#rule-timezone) -->
[After](#rule-after)
[After Or Equal](#rule-after-or-equal)
[Before](#rule-before)
[Before Or Equal](#rule-before-or-equal)
[Date](#rule-date)
[Date Equals](#rule-date-equals)
[Date Format](#rule-date-format)
[Different](#rule-different)
[Timezone](#rule-timezone)

</div>

<!-- #### Files -->
#### Files

<div class="collection-method-list" markdown="1">

<!-- [Between](#rule-between) [Dimensions](#rule-dimensions) [Encoding](#rule-encoding) [Extensions](#rule-extensions) [File](#rule-file) [Image](#rule-image) [Max](#rule-max) [Min](#rule-min) [MIME Types](#rule-mimetypes) [MIME Type By File Extension](#rule-mimes) [Size](#rule-size) -->
[Between](#rule-between)
[Dimensions](#rule-dimensions)
[Encoding](#rule-encoding)
[Extensions](#rule-extensions)
[File](#rule-file)
[Image](#rule-image)
[Max](#rule-max)
[Min](#rule-min)
[MIME Types](#rule-mimetypes)
[MIME Type By File Extension](#rule-mimes)
[Size](#rule-size)

</div>

<!-- #### Database -->
#### Database

<div class="collection-method-list" markdown="1">

<!-- [Exists](#rule-exists) [Unique](#rule-unique) -->
[Exists](#rule-exists)
[Unique](#rule-unique)

</div>

<!-- #### Utilities -->
#### Utilities

<div class="collection-method-list" markdown="1">

<!-- [Any Of](#rule-anyof) [Bail](#rule-bail) [Exclude](#rule-exclude) [Exclude If](#rule-exclude-if) [Exclude Unless](#rule-exclude-unless) [Exclude With](#rule-exclude-with) [Exclude Without](#rule-exclude-without) [Filled](#rule-filled) [Missing](#rule-missing) [Missing If](#rule-missing-if) [Missing Unless](#rule-missing-unless) [Missing With](#rule-missing-with) [Missing With All](#rule-missing-with-all) [Nullable](#rule-nullable) [Present](#rule-present) [Present If](#rule-present-if) [Present Unless](#rule-present-unless) [Present With](#rule-present-with) [Present With All](#rule-present-with-all) [Prohibited](#rule-prohibited) [Prohibited If](#rule-prohibited-if) [Prohibited If Accepted](#rule-prohibited-if-accepted) [Prohibited If Declined](#rule-prohibited-if-declined) [Prohibited Unless](#rule-prohibited-unless) [Prohibits](#rule-prohibits) [Required](#rule-required) [Required If](#rule-required-if) [Required If Accepted](#rule-required-if-accepted) [Required If Declined](#rule-required-if-declined) [Required Unless](#rule-required-unless) [Required With](#rule-required-with) [Required With All](#rule-required-with-all) [Required Without](#rule-required-without) [Required Without All](#rule-required-without-all) [Required Array Keys](#rule-required-array-keys) [Sometimes](#validating-when-present) -->
[Any Of](#rule-anyof)
[Bail](#rule-bail)
[Exclude](#rule-exclude)
[Exclude If](#rule-exclude-if)
[Exclude Unless](#rule-exclude-unless)
[Exclude With](#rule-exclude-with)
[Exclude Without](#rule-exclude-without)
[Filled](#rule-filled)
[Missing](#rule-missing)
[Missing If](#rule-missing-if)
[Missing Unless](#rule-missing-unless)
[Missing With](#rule-missing-with)
[Missing With All](#rule-missing-with-all)
[Nullable](#rule-nullable)
[Present](#rule-present)
[Present If](#rule-present-if)
[Present Unless](#rule-present-unless)
[Present With](#rule-present-with)
[Present With All](#rule-present-with-all)
[Prohibited](#rule-prohibited)
[Prohibited If](#rule-prohibited-if)
[Prohibited If Accepted](#rule-prohibited-if-accepted)
[Prohibited If Declined](#rule-prohibited-if-declined)
[Prohibited Unless](#rule-prohibited-unless)
[Prohibits](#rule-prohibits)
[Required](#rule-required)
[Required If](#rule-required-if)
[Required If Accepted](#rule-required-if-accepted)
[Required If Declined](#rule-required-if-declined)
[Required Unless](#rule-required-unless)
[Required With](#rule-required-with)
[Required With All](#rule-required-with-all)
[Required Without](#rule-required-without)
[Required Without All](#rule-required-without-all)
[Required Array Keys](#rule-required-array-keys)
[Sometimes](#validating-when-present)

</div>

<a name="rule-accepted"></a>
<!-- #### accepted -->
#### accepted

<!-- The field under validation must be `"yes"`, `"on"`, `1`, `"1"`, `true`, or `"true"`. This is useful for validating "Terms of Service" acceptance or similar fields. -->
検証対象のフィールドは、`"yes"`、`"on"`、`1`、`"1"`、`true`、または `"true"` である必要があります。これは、「利用規約」への同意または同様のフィールドを検証するのに役立ちます。

<a name="rule-accepted-if"></a>
<!-- #### accepted_if:anotherfield,value,... -->
#### accepted_if:anotherfield,value,...

<!-- The field under validation must be `"yes"`, `"on"`, `1`, `"1"`, `true`, or `"true"` if another field under validation is equal to a specified value. This is useful for validating "Terms of Service" acceptance or similar fields. -->
検証中の別のフィールドが指定された値と等しい場合、検証中のフィールドは `"yes"`、`"on"`、`1`、`"1"`、`true`、または `"true"` である必要があります。これは、「利用規約」への同意または同様のフィールドを検証するのに役立ちます。

<a name="rule-active-url"></a>
<!-- #### active_url -->
#### active_url

<!-- The field under validation must have a valid A or AAAA record according to the `dns_get_record` PHP function. The hostname of the provided URL is extracted using the `parse_url` PHP function before being passed to `dns_get_record`. -->
検証対象のフィールドには、`dns_get_record` PHP 関数に従って、有効な A または AAAA レコードが必要です。指定された URL のホスト名は、`dns_get_record` に渡される前に、`parse_url` PHP 関数を使用して抽出されます。

<!-- When testing validation rules that perform DNS lookups, such as `active_url` and `email:dns`, you may use the `Validator::fakeDnsLookups` method. This fakes DNS lookups while preserving the rules' other validation behavior: -->
`active_url` や `email:dns` など、DNS ルックアップを実行するバリデーションルールをテストする場合は、`Validator::fakeDnsLookups` メソッドを使用できます。このメソッドは、ルールによるその他のバリデーション処理を維持したまま、DNS ルックアップを偽装します。

```php
use Illuminate\Support\Facades\Validator;

Validator::fakeDnsLookups();
```

<a name="rule-after"></a>
<!-- #### after:_date_ -->
#### after:_date_

<!-- The field under validation must be a value after a given date. The dates will be passed into the `strtotime` PHP function in order to be converted to a valid `DateTime` instance: -->
検証対象のフィールドは、指定された日付以降の値である必要があります。日付は、有効な `DateTime` インスタンスに変換されるために、`strtotime` PHP 関数に渡されます。

```php
'start_date' => ['required', 'date', 'after:tomorrow']
```

<!-- Instead of passing a date string to be evaluated by `strtotime`, you may specify another field to compare against the date: -->
`strtotime` によって評価される日付文字列を渡す代わりに、日付と比較する別のフィールドを指定できます。

```php
'finish_date' => ['required', 'date', 'after:start_date']
```

<!-- For convenience, date-based rules may be constructed using the fluent `date` rule builder: -->
便宜上、日付ベースのルールは、滑らかな `date` ルール ビルダを使用して構築できます。

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->after(today()->addDays(7)),
],
```

<!-- The `afterToday` and `todayOrAfter` methods may be used to fluently express the date and must be after today, or today or after, respectively: -->
`afterToday` メソッドと `todayOrAfter` メソッドは日付をスムーズに表現するために使用でき、それぞれ今日以降、または今日以降である必要があります。

```php
'start_date' => [
    'required',
    Rule::date()->afterToday(),
],
```

<a name="rule-after-or-equal"></a>
<!-- #### after\_or\_equal:_date_ -->
#### after\_or\_equal:_date_

<!-- The field under validation must be a value after or equal to the given date. For more information, see the [after](#rule-after) rule. -->
検証対象のフィールドは、指定された日付以降の値である必要があります。詳細については、[after](#rule-after) ルールを参照してください。

<!-- For convenience, date-based rules may be constructed using the fluent `date` rule builder: -->
便宜上、日付ベースのルールは、滑らかな `date` ルール ビルダを使用して構築できます。

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->afterOrEqual(today()->addDays(7)),
],
```

<a name="rule-anyof"></a>
<!-- #### anyOf -->
#### anyOf

<!-- The `Rule::anyOf` validation rule allows you to specify that the field under validation must satisfy any of the given validation rulesets. For example, the following rule will validate that the `username` field is either an email address or an alpha-numeric string (including dashes) that is at least 6 characters long: -->
`Rule::anyOf` 検証ルールを使用すると、検証対象のフィールドが指定された検証ルールセットのいずれかを満たす必要があることを指定できます。たとえば、次のルールは、`username` フィールドが電子メール アドレスであるか、または少なくとも 6 文字の長さの英数字文字列 (ダッシュを含む) であることを検証します。

```php
use Illuminate\Validation\Rule;

'username' => [
    'required',
    Rule::anyOf([
        ['string', 'email'],
        ['string', 'alpha_dash', 'min:6'],
    ]),
],
```

<a name="rule-alpha"></a>
<!-- #### alpha -->
#### alpha

<!-- The field under validation must be entirely Unicode alphabetic characters contained in [\p{L}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=) and [\p{M}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=). -->
検証対象のフィールドは、[\p{L}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=) および [\p{M}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=) に含まれる完全に Unicode アルファベット文字である必要があります。

<!-- To restrict this validation rule to characters in the ASCII range (`a-z` and `A-Z`), you may provide the `ascii` option to the validation rule: -->
この検証ルールを ASCII 範囲の文字 (`a-z` および `A-Z`) に制限するには、検証ルールに `ascii` オプションを指定します。

```php
'username' => ['alpha:ascii'],
```

<a name="rule-alpha-dash"></a>
<!-- #### alpha_dash -->
#### alpha_dash

<!-- The field under validation must be entirely Unicode alpha-numeric characters contained in [\p{L}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=), [\p{M}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=), [\p{N}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AN%3A%5D&g=&i=), as well as ASCII dashes (`-`) and ASCII underscores (`_`). -->
検証対象のフィールドは、[\p{L}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=)、[\p{M}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=)、[\p{N}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AN%3A%5D&g=&i=)、ASCII ダッシュ (`-`) および ASCII アンダースコア (`_`) に含まれる完全に Unicode の英数字である必要があります。

<!-- To restrict this validation rule to characters in the ASCII range (`a-z`, `A-Z`, and `0-9`), you may provide the `ascii` option to the validation rule: -->
この検証ルールを ASCII 範囲の文字 (`a-z`、`A-Z`、および `0-9`) に制限するには、検証ルールに `ascii` オプションを指定できます。

```php
'username' => ['alpha_dash:ascii'],
```

<a name="rule-alpha-num"></a>
<!-- #### alpha_num -->
#### alpha_num

<!-- The field under validation must be entirely Unicode alpha-numeric characters contained in [\p{L}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=), [\p{M}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=), and [\p{N}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AN%3A%5D&g=&i=). -->
検証対象のフィールドは、[\p{L}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=)、[\p{M}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=)、および [\p{N}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AN%3A%5D&g=&i=) に含まれる完全に Unicode の英数字である必要があります。

<!-- To restrict this validation rule to characters in the ASCII range (`a-z`, `A-Z`, and `0-9`), you may provide the `ascii` option to the validation rule: -->
この検証ルールを ASCII 範囲の文字 (`a-z`、`A-Z`、および `0-9`) に制限するには、検証ルールに `ascii` オプションを指定できます。

```php
'username' => ['alpha_num:ascii'],
```

<a name="rule-array"></a>
<!-- #### array -->
#### array

<!-- The field under validation must be a PHP `array`. -->
検証対象のフィールドは PHP `array` である必要があります。

<!-- When additional values are provided to the `array` rule, each key in the input array must be present within the list of values provided to the rule. In the following example, the `admin` key in the input array is invalid since it is not contained in the list of values provided to the `array` rule: -->
追加の値が `array` ルールに指定される場合、入力配列内の各キーがルールに指定される値のリスト内に存在する必要があります。次の例では、入力配列の `admin` キーは、`array` ルールに提供される値のリストに含まれていないため、無効です。

```php
use Illuminate\Support\Facades\Validator;

$input = [
    'user' => [
        'name' => 'Taylor Otwell',
        'username' => 'taylorotwell',
        'admin' => true,
    ],
];

Validator::make($input, [
    'user' => ['array:name,username'],
]);
```

<!-- In general, you should always specify the array keys that are allowed to be present within your array. -->
一般に、配列内に存在できる配列キーを常に指定する必要があります。

<a name="rule-array-keys"></a>
<!-- #### array_keys:_foo_,_bar_,... -->
#### array_keys:_foo_,_bar_,...

<!-- The field under validation must be a PHP `array` whose keys are all included in the given list. At least one key must be provided: -->
バリデーション対象のフィールドは PHP の `array` であり、そのキーがすべて指定したリストに含まれていなければなりません。少なくとも1つのキーを指定する必要があります。

```php
'user' => ['array_keys:name,username'],
```

<!-- For convenience, you may use the `Rule::arrayKeys` method: -->
便利な方法として、`Rule::arrayKeys` メソッドを使用することもできます。

```php
'user' => [Rule::arrayKeys('name', 'username')],
```

<a name="rule-ascii"></a>
<!-- #### ascii -->
#### ascii

<!-- The field under validation must be entirely 7-bit ASCII characters. -->
検証対象のフィールドは完全に 7 ビット ASCII 文字である必要があります。

<a name="rule-bail"></a>
<!-- #### bail -->
#### bail

<!-- Stop running validation rules for the field after the first validation failure. -->
最初の検証が失敗した後は、フィールドの検証ルールの実行を停止します。

<!-- While the `bail` rule will only stop validating a specific field when it encounters a validation failure, the `stopOnFirstFailure` method will inform the validator that it should stop validating all attributes once a single validation failure has occurred: -->
`bail` ルールは検証エラーが発生した場合にのみ特定のフィールドの検証を停止しますが、`stopOnFirstFailure` メソッドは、単一の検証エラーが発生するとすべての属性の検証を停止する必要があることをバリデーターに通知します。

```php
if ($validator->stopOnFirstFailure()->fails()) {
    // ...
}
```

<a name="rule-before"></a>
<!-- #### before:_date_ -->
#### before:_date_

<!-- The field under validation must be a value preceding the given date. The dates will be passed into the PHP `strtotime` function in order to be converted into a valid `DateTime` instance. In addition, like the [after](#rule-after) rule, the name of another field under validation may be supplied as the value of `date`. -->
検証対象のフィールドは、指定された日付より前の値である必要があります。日付は、有効な `DateTime` インスタンスに変換されるために、PHP `strtotime` 関数に渡されます。さらに、[after](#rule-after) ルールと同様に、検証中の別のフィールドの名前を `date` の値として指定することもできます。

<!-- For convenience, date-based rules may also be constructed using the fluent `date` rule builder: -->
便宜上、日付ベースのルールは、滑らかな `date` ルール ビルダを使用して構築することもできます。

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->before(today()->subDays(7)),
],
```

<!-- The `beforeToday` and `todayOrBefore` methods may be used to fluently express the date and must be before today, or today or before, respectively: -->
`beforeToday` メソッドと `todayOrBefore` メソッドは日付をスムーズに表現するために使用でき、それぞれ今日より前、または今日以前である必要があります。

```php
'start_date' => [
    'required',
    Rule::date()->beforeToday(),
],
```

<a name="rule-before-or-equal"></a>
<!-- #### before\_or\_equal:_date_ -->
#### before\_or\_equal:_date_

<!-- The field under validation must be a value preceding or equal to the given date. The dates will be passed into the PHP `strtotime` function in order to be converted into a valid `DateTime` instance. In addition, like the [after](#rule-after) rule, the name of another field under validation may be supplied as the value of `date`. -->
検証対象のフィールドは、指定された日付以前の値である必要があります。日付は、有効な `DateTime` インスタンスに変換されるために、PHP `strtotime` 関数に渡されます。さらに、[after](#rule-after) ルールと同様に、検証中の別のフィールドの名前を `date` の値として指定することもできます。

<!-- For convenience, date-based rules may also be constructed using the fluent `date` rule builder: -->
便宜上、日付ベースのルールは、滑らかな `date` ルール ビルダを使用して構築することもできます。

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->beforeOrEqual(today()->subDays(7)),
],
```

<a name="rule-between"></a>
<!-- #### between:_min_,_max_ -->
#### between:_min_,_max_

<!-- The field under validation must have a size between the given _min_ and _max_ (inclusive). Strings, numerics, arrays, and files are evaluated in the same fashion as the [size](#rule-size) rule. -->
検証中のフィールドのサイズは、指定された _min_ と _max_ (両端を含む) の間である必要があります。文字列、数値、配列、ファイルは、[size](#rule-size) ルールと同じ方法で評価されます。

<a name="rule-boolean"></a>
<!-- #### boolean -->
#### boolean

<!-- The field under validation must be able to be cast as a boolean. Accepted input are `true`, `false`, `1`, `0`, `"1"`, and `"0"`. -->
検証中のフィールドはブール値としてcastできる必要があります。受け入れられる入力は、`true`、`false`、`1`、`0`、`"1"`、および `"0"` です。

<!-- You may use the `strict` parameter to only consider the field valid if its value is `true` or `false`: -->
`strict` パラメータを使用すると、値が `true` または `false` の場合にのみフィールドが有効であると見なすことができます。

```php
'foo' => ['boolean:strict']
```

<a name="rule-confirmed"></a>
<!-- #### confirmed -->
#### confirmed

<!-- The field under validation must have a matching field of `{field}_confirmation`. For example, if the field under validation is `password`, a matching `password_confirmation` field must be present in the input. -->
検証中のフィールドには、`{field}_confirmation` の一致するフィールドが必要です。たとえば、検証対象のフィールドが `password` の場合、一致する `password_confirmation` フィールドが入力に存在する必要があります。

<!-- You may also pass a custom confirmation field name. For example, `confirmed:repeat_username` will expect the field `repeat_username` to match the field under validation. -->
カスタム確認フィールド名を渡すこともできます。たとえば、`confirmed:repeat_username` は、フィールド `repeat_username` が検証中のフィールドと一致することを期待します。

<a name="rule-contains"></a>
<!-- #### contains:_foo_,_bar_,... -->
#### contains:_foo_,_bar_,...

<!-- The field under validation must be an array that contains all of the given parameter values. Since this rule often requires you to `implode` an array, the `Rule::contains` method may be used to fluently construct the rule: -->
検証対象のフィールドは、指定されたパラメータ値をすべて含む配列である必要があります。このルールでは配列を `implode` する必要があることが多いため、ルールをスムーズに構築するために `Rule::contains` メソッドを使用できます。

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($data, [
    'roles' => [
        'required',
        'array',
        Rule::contains(['admin', 'editor']),
    ],
]);
```

<a name="rule-doesnt-contain"></a>
<!-- #### doesnt_contain:_foo_,_bar_,... -->
#### doesnt_contain:_foo_,_bar_,...

<!-- The field under validation must be an array that does not contain any of the given parameter values. Since this rule often requires you to `implode` an array, the `Rule::doesntContain` method may be used to fluently construct the rule: -->
検証対象のフィールドは、指定されたパラメータ値を含まない配列である必要があります。このルールでは配列を `implode` する必要があることが多いため、ルールをスムーズに構築するために `Rule::doesntContain` メソッドを使用できます。

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($data, [
    'roles' => [
        'required',
        'array',
        Rule::doesntContain(['admin', 'editor']),
    ],
]);
```

<a name="rule-current-password"></a>
<!-- #### current_password -->
#### current_password

<!-- The field under validation must match the authenticated user's password. You may specify an [authentication guard](/docs/13.x/authentication) using the rule's first parameter: -->
検証中のフィールドは、認証されたユーザーのパスワードと一致する必要があります。ルールの最初のパラメータを使用して、[authentication guard](/docs/13.x/authentication) を指定できます。

```php
'password' => ['current_password:api']
```

<a name="rule-date"></a>
<!-- #### date -->
#### date

<!-- The field under validation must be a valid, non-relative date according to the `strtotime` PHP function. -->
検証対象のフィールドは、`strtotime` PHP 関数に従って、有効な非相対日付である必要があります。

<a name="rule-date-equals"></a>
<!-- #### date_equals:_date_ -->
#### date_equals:_date_

<!-- The field under validation must be equal to the given date. The dates will be passed into the PHP `strtotime` function in order to be converted into a valid `DateTime` instance. -->
検証対象のフィールドは、指定された日付と一致する必要があります。日付は、有効な `DateTime` インスタンスに変換されるために、PHP `strtotime` 関数に渡されます。

<a name="rule-date-format"></a>
<!-- #### date_format:_format_,... -->
#### date_format:_format_,...

<!-- The field under validation must match one of the given _formats_. You should use **either** `date` or `date_format` when validating a field, not both. This validation rule supports all formats supported by PHP's [DateTime](https://www.php.net/manual/en/class.datetime.php) class. -->
検証中のフィールドは、指定された_formats_のいずれかに一致する必要があります。フィールドを検証するときは、`date` または `date_format` の両方ではなく、**どちらか** を使用する必要があります。この検証ルールは、PHP の [DateTime](https://www.php.net/manual/en/class.datetime.php) クラスでサポートされるすべての形式をサポートします。

<!-- For convenience, date-based rules may be constructed using the fluent `date` rule builder: -->
便宜上、日付ベースのルールは、滑らかな `date` ルール ビルダを使用して構築できます。

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->format('Y-m-d'),
],
```

<a name="rule-decimal"></a>
<!-- #### decimal:_min_,_max_ -->
#### decimal:_min_,_max_

<!-- The field under validation must be numeric and must contain the specified number of decimal places: -->
検証対象のフィールドは数値である必要があり、指定された小数点以下の桁数が含まれている必要があります。

```php
// Must have exactly two decimal places (9.99)...
'price' => ['decimal:2']

// Must have between 2 and 4 decimal places...
'price' => ['decimal:2,4']
```

<a name="rule-declined"></a>
<!-- #### declined -->
#### declined

<!-- The field under validation must be `"no"`, `"off"`, `0`, `"0"`, `false`, or `"false"`. -->
検証対象のフィールドは、`"no"`、`"off"`、`0`、`"0"`、`false`、または `"false"` である必要があります。

<a name="rule-declined-if"></a>
<!-- #### declined_if:anotherfield,value,... -->
#### declined_if:anotherfield,value,...

<!-- The field under validation must be `"no"`, `"off"`, `0`, `"0"`, `false`, or `"false"` if another field under validation is equal to a specified value. -->
検証中の別のフィールドが指定された値と等しい場合、検証中のフィールドは `"no"`、`"off"`、`0`、`"0"`、`false`、または `"false"` である必要があります。

<a name="rule-different"></a>
<!-- #### different:_field_ -->
#### different:_field_

<!-- The field under validation must have a different value than _field_. -->
検証中のフィールドは、_field_ とは異なる値を持つ必要があります。

<a name="rule-digits"></a>
<!-- #### digits:_value_ -->
#### digits:_value_

<!-- The integer under validation must have an exact length of _value_. -->
検証される整数は、_value_ の正確な長さである必要があります。

<a name="rule-digits-between"></a>
<!-- #### digits_between:_min_,_max_ -->
#### digits_between:_min_,_max_

<!-- The integer under validation must have a length between the given _min_ and _max_. -->
検証される整数は、指定された _min_ と _max_ の間の長さでなければなりません。

<a name="rule-dimensions"></a>
<!-- #### dimensions -->
#### dimensions

<!-- The file under validation must be an image meeting the dimension constraints as specified by the rule's parameters: -->
検証中のファイルは、ルールのパラメータで指定された寸法制約を満たす画像である必要があります。

```php
'avatar' => ['dimensions:min_width=100,min_height=200']
```

<!-- Available constraints are: _min\_width_, _max\_width_, _min\_height_, _max\_height_, _width_, _height_, _ratio_, _min\_ratio_, _max\_ratio_. -->
使用可能な制約は、_min\_width_、_max\_width_、_min\_height_、_max\_height_、_width_、_height_、_ratio_、_min\_ratio_、_max\_ratio_ です。

<!-- A _ratio_ constraint should be represented as width divided by height. This can be specified either by a fraction like `3/2` or a float like `1.5`: -->
_ratio_ 制約は、幅を高さで割ったものとして表す必要があります。これは、`3/2` のような分数または `1.5` のような浮動小数点数のいずれかで指定できます。

```php
'avatar' => ['dimensions:ratio=3/2']
```

<!-- The _min\_ratio_ and _max\_ratio_ constraints may be used to define a range of acceptable aspect ratios: -->
_min\_ratio_ および _max\_ratio_ 制約を使用して、許容されるアスペクト比の範囲を定義できます。

```php
'avatar' => ['dimensions:min_ratio=1/2,max_ratio=3/2']
```

<!-- Since this rule requires several arguments, it is often more convenient to use the `Rule::dimensions` method to fluently construct the rule: -->
このルールには複数の引数が必要なため、多くの場合、`Rule::dimensions` メソッドを使用してルールをスムーズに構築する方が便利です。

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($data, [
    'avatar' => [
        'required',
        Rule::dimensions()
            ->maxWidth(1000)
            ->maxHeight(500)
            ->ratio(3 / 2),
    ],
]);
```

<!-- You may also use the `minRatio`, `maxRatio`, and `ratioBetween` methods to fluently define ratio constraints: -->
`minRatio`、`maxRatio`、および `ratioBetween` メソッドを使用して、比率制約をスムーズに定義することもできます。

```php
Rule::dimensions()->ratioBetween(min: 1 / 2, max: 3 / 2)
```

<a name="rule-distinct"></a>
<!-- #### distinct -->
#### distinct

<!-- When validating arrays, the field under validation must not have any duplicate values: -->
配列を検証する場合、検証対象のフィールドに重複する値があってはなりません。

```php
'foo.*.id' => ['distinct']
```

<!-- Distinct uses loose variable comparisons by default. To use strict comparisons, you may add the `strict` parameter to your validation rule definition: -->
Distinct は、デフォルトで緩い変数比較を使用します。厳密な比較を使用するには、検証ルール定義に `strict` パラメータを追加します。

```php
'foo.*.id' => ['distinct:strict']
```

<!-- You may add `ignore_case` to the validation rule's arguments to make the rule ignore capitalization differences: -->
検証ルールの引数に `ignore_case` を追加して、大文字と小文字の違いをルールに無視させることができます。

```php
'foo.*.id' => ['distinct:ignore_case']
```

<a name="rule-doesnt-start-with"></a>
<!-- #### doesnt_start_with:_foo_,_bar_,... -->
#### doesnt_start_with:_foo_,_bar_,...

<!-- The field under validation must not start with one of the given values. -->
検証中のフィールドは、指定された値のいずれかで始まってはなりません。

<a name="rule-doesnt-end-with"></a>
<!-- #### doesnt_end_with:_foo_,_bar_,... -->
#### doesnt_end_with:_foo_,_bar_,...

<!-- The field under validation must not end with one of the given values. -->
検証中のフィールドは、指定された値のいずれかで終わってはいけません。

<a name="rule-email"></a>
<!-- #### email -->
#### email

<!-- The field under validation must be formatted as an email address. This validation rule utilizes the [egulias/email-validator](https://github.com/egulias/EmailValidator) package for validating the email address. By default, the `RFCValidation` validator is applied, but you can apply other validation styles as well: -->
検証中のフィールドは電子メール アドレスとしてフォーマットされている必要があります。この検証ルールは、電子メール アドレスを検証するために [egulias/email-validator](https://github.com/egulias/EmailValidator) パッケージを利用します。デフォルトでは、`RFCValidation` バリデーターが適用されますが、他の検証スタイルも適用できます。

```php
'email' => ['email:rfc,dns']
```

<!-- The example above will apply the `RFCValidation` and `DNSCheckValidation` validations. Here's a full list of validation styles you can apply: -->
上記の例では、`RFCValidation` 検証と `DNSCheckValidation` 検証を適用します。適用できる検証スタイルの完全なリストは次のとおりです。

<div class="content-list" markdown="1">

<!-- - `rfc`: `RFCValidation` - Validate the email address according to [supported RFCs](https://github.com/egulias/EmailValidator?tab=readme-ov-file#supported-rfcs). - `strict`: `NoRFCWarningsValidation` - Validate the email according to [supported RFCs](https://github.com/egulias/EmailValidator?tab=readme-ov-file#supported-rfcs), failing when warnings are found (e.g. trailing periods and multiple consecutive periods). - `dns`: `DNSCheckValidation` - Ensure the email address's domain has a valid MX record. - `spoof`: `SpoofCheckValidation` - Ensure the email address does not contain homograph or deceptive Unicode characters. - `filter`: `FilterEmailValidation` - Ensure the email address is valid according to PHP's `filter_var` function. - `filter_unicode`: `FilterEmailValidation::unicode()` - Ensure the email address is valid according to PHP's `filter_var` function, allowing some Unicode characters. -->
- `rfc`: `RFCValidation` - [supported RFCs](https://github.com/egulias/EmailValidator?tab=readme-ov-file#supported-rfcs) に従って電子メール アドレスを検証します。
- `strict`: `NoRFCWarningsValidation` - [supported RFCs](https://github.com/egulias/EmailValidator?tab=readme-ov-file#supported-rfcs) に従って電子メールを検証し、警告 (例: 末尾のピリオドや複数の連続するピリオド) が見つかった場合は失敗します。
- `dns`: `DNSCheckValidation` - 電子メール アドレスのドメインに有効な MX レコードがあることを確認します。
- `spoof`: `SpoofCheckValidation` - 電子メール アドレスに同形異義語や欺瞞的な Unicode 文字が含まれていないことを確認してください。
- `filter`: `FilterEmailValidation` - 電子メール アドレスが PHP の `filter_var` 関数に従って有効であることを確認します。
- `filter_unicode`: `FilterEmailValidation::unicode()` - 電子メール アドレスが PHP の `filter_var` 関数に従って有効であることを確認し、一部の Unicode 文字を許可します。

</div>

<!-- For convenience, email validation rules may be built using the fluent rule builder: -->
便宜上、電子メール検証ルールは Fluent ルール ビルダを使用して構築できます。

```php
use Illuminate\Validation\Rule;

$request->validate([
    'email' => [
        'required',
        Rule::email()
            ->rfcCompliant(strict: false)
            ->validateMxRecord()
            ->preventSpoofing()
    ],
]);
```

<!-- The `dns` validator performs a real DNS lookup to confirm the address's domain has a valid MX record. It does not determine whether an individual mailbox exists. -->
`dns` バリデータは実際に DNS ルックアップを実行し、アドレスのドメインに有効な MX レコードがあることを確認します。個々のメールボックスが存在するかどうかは判定しません。

<!-- Since your tests should not rely on live DNS lookups, you may use the `Validator::fakeDnsLookups` method to [fake DNS lookups](#rule-active-url) while any other requested validations, such as `rfc`, continue to run: -->
テストでは実際の DNS ルックアップに依存しないようにする必要があるため、`Validator::fakeDnsLookups` メソッドを使って [fake DNS lookups](#rule-active-url) を実行し、`rfc` など、指定したほかのバリデーションは通常どおり実行できます。

```php
use Illuminate\Support\Facades\Validator;

Validator::fakeDnsLookups();
```

<!-- This allows your application to keep using its existing validation rules while testing: -->
これにより、テスト中もアプリケーションで既存のバリデーションルールを使い続けられます。

```php
'email' => ['required', 'email:rfc,dns'],
```

> [!WARNING]
> `dns` および `spoof` バリデーターには、PHP `intl` 拡張機能が必要です。

<a name="rule-encoding"></a>
<!-- #### encoding:*encoding_type* -->
#### encoding:*encoding_type*

<!-- The field under validation must match the specified character encoding. This rule uses PHP's `mb_check_encoding` function to verify the encoding of the given file or string value. For convenience, the `encoding` rule may be constructed using Laravel's fluent file rule builder: -->
検証対象のフィールドは、指定された文字エンコーディングと一致する必要があります。このルールは、PHP の `mb_check_encoding` 関数を使用して、指定されたファイルまたは文字列値のエンコードを検証します。便宜上、`encoding` ルールは、Laravel の Fluent ファイル ルール ビルダを使用して構築できます。

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rules\File;

Validator::validate($input, [
    'attachment' => [
        'required',
        File::types(['csv'])
            ->encoding('utf-8'),
    ],
]);
```

<a name="rule-ends-with"></a>
<!-- #### ends_with:_foo_,_bar_,... -->
#### ends_with:_foo_,_bar_,...

<!-- The field under validation must end with one of the given values. -->
検証中のフィールドは、指定された値のいずれかで終わる必要があります。

<a name="rule-enum"></a>
<!-- #### enum -->
#### enum

<!-- The `Enum` rule is a class-based rule that validates whether the field under validation contains a valid enum value. The `Enum` rule accepts the name of the enum as its only constructor argument. When validating primitive values, a backed Enum should be provided to the `Enum` rule: -->
`Enum` ルールは、検証対象のフィールドに有効な列挙値が含まれているかどうかを検証するクラスベースのルールです。 `Enum` ルールは、列挙型の名前を唯一のコンストラクター引数として受け入れます。プリミティブ値を検証するときは、裏付けされた Enum を `Enum` ルールに提供する必要があります。

```php
use App\Enums\ServerStatus;
use Illuminate\Validation\Rule;

$request->validate([
    'status' => [Rule::enum(ServerStatus::class)],
]);
```

<!-- The `Enum` rule's `only` and `except` methods may be used to limit which enum cases should be considered valid: -->
`Enum` ルールの `only` メソッドと `except` メソッドを使用して、有効とみなされる列挙型ケースを制限できます。

```php
Rule::enum(ServerStatus::class)
    ->only([ServerStatus::Pending, ServerStatus::Active]);

Rule::enum(ServerStatus::class)
    ->except([ServerStatus::Pending, ServerStatus::Active]);
```

<!-- The `when` method may be used to conditionally modify the `Enum` rule: -->
`when` メソッドは、条件付きで `Enum` ルールを変更するために使用できます。

```php
use Illuminate\Support\Facades\Auth;
use Illuminate\Validation\Rule;

Rule::enum(ServerStatus::class)
    ->when(
        Auth::user()->isAdmin(),
        fn ($rule) => $rule->only(...),
        fn ($rule) => $rule->only(...),
    );
```

<a name="rule-exclude"></a>
<!-- #### exclude -->
#### exclude

<!-- The field under validation will be excluded from the request data returned by the `validate` and `validated` methods. -->
検証中のフィールドは、`validate` メソッドおよび `validated` メソッドによって返されるリクエスト データから除外されます。

<a name="rule-exclude-if"></a>
<!-- #### exclude_if:_anotherfield_,_value_ -->
#### exclude_if:_anotherfield_,_value_

<!-- The field under validation will be excluded from the request data returned by the `validate` and `validated` methods if the _anotherfield_ field is equal to _value_. -->
_anotherfield_ フィールドが _value_ と等しい場合、検証中のフィールドは、`validate` メソッドおよび `validated` メソッドによって返されるリクエスト データから除外されます。

<!-- If complex conditional exclusion logic is required, you may utilize the `Rule::excludeIf` method. This method accepts a boolean or a closure. When given a closure, the closure should return `true` or `false` to indicate if the field under validation should be excluded: -->
複雑な条件付き除外ロジックが必要な場合は、`Rule::excludeIf` メソッドを利用できます。このメソッドはブール値またはクロージャを受け入れます。クロージャが指定された場合、クロージャは `true` または `false` を返し、検証中のフィールドを除外する必要があるかどうかを示す必要があります。

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($request->all(), [
    'role_id' => [Rule::excludeIf($request->user()->is_admin)],
]);

Validator::make($request->all(), [
    'role_id' => [Rule::excludeIf(fn () => $request->user()->is_admin)],
]);
```

<a name="rule-exclude-unless"></a>
<!-- #### exclude_unless:_anotherfield_,_value_ -->
#### exclude_unless:_anotherfield_,_value_

<!-- The field under validation will be excluded from the request data returned by the `validate` and `validated` methods unless _anotherfield_'s field is equal to _value_. If _value_ is `null` (`exclude_unless:name,null`), the field under validation will be excluded unless the comparison field is `null` or the comparison field is missing from the request data. -->
検証中のフィールドは、_anotherfield_ のフィールドが _value_ と等しい場合を除き、`validate` メソッドおよび `validated` メソッドによって返されるリクエスト データから除外されます。 _value_ が `null` (`exclude_unless:name,null`) の場合、比較フィールドが `null` でない限り、または比較フィールドがリクエスト データに欠落している場合を除き、検証対象のフィールドは除外されます。

<!-- If complex conditional exclusion logic is required, you may utilize the `Rule::excludeUnless` method. This method accepts a boolean or a closure. When given a closure, the closure should return `true` or `false` to indicate if the field under validation should not be excluded: -->
複雑な条件付き除外ロジックが必要な場合は、`Rule::excludeUnless` メソッドを利用できます。このメソッドはブール値またはクロージャを受け入れます。クロージャが指定された場合、クロージャは `true` または `false` を返し、検証中のフィールドを除外すべきかどうかを示す必要があります。

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($request->all(), [
    'role_id' => [Rule::excludeUnless($request->user()->is_admin)],
]);

Validator::make($request->all(), [
    'role_id' => [Rule::excludeUnless(fn () => $request->user()->is_admin)],
]);
```

<a name="rule-exclude-with"></a>
<!-- #### exclude_with:_anotherfield_ -->
#### exclude_with:_anotherfield_

<!-- The field under validation will be excluded from the request data returned by the `validate` and `validated` methods if the _anotherfield_ field is present. -->
_anotherfield_ フィールドが存在する場合、検証中のフィールドは、`validate` メソッドおよび `validated` メソッドによって返されるリクエスト データから除外されます。

<a name="rule-exclude-without"></a>
<!-- #### exclude_without:_anotherfield_ -->
#### exclude_without:_anotherfield_

<!-- The field under validation will be excluded from the request data returned by the `validate` and `validated` methods if the _anotherfield_ field is not present. -->
_anotherfield_ フィールドが存在しない場合、検証中のフィールドは、`validate` および `validated` メソッドによって返されるリクエスト データから除外されます。

<a name="rule-exists"></a>
<!-- #### exists:_table_,_column_ -->
#### exists:_table_,_column_

<!-- The field under validation must exist in a given database table. -->
検証対象のフィールドは、特定のデータベース テーブルに存在する必要があります。

<a name="basic-usage-of-exists-rule"></a>
<!-- #### Basic Usage of Exists Rule -->
#### Basic Usage of Exists Rule

```php
'state' => ['exists:states']
```

<!-- If the `column` option is not specified, the field name will be used. So, in this case, the rule will validate that the `states` database table contains a record with a `state` column value matching the request's `state` attribute value. -->
`column` オプションが指定されていない場合は、フィールド名が使用されます。したがって、この場合、ルールは、`states` データベース テーブルに、リクエストの `state` 属性値と一致する `state` 列値を持つレコードが含まれていることを検証します。

<a name="specifying-a-custom-column-name"></a>
<!-- #### Specifying a Custom Column Name -->
#### Specifying a Custom Column Name

<!-- You may explicitly specify the database column name that should be used by the validation rule by placing it after the database table name: -->
データベーステーブル名の後に置くことで、検証ルールで使用するデータベース列名を明示的に指定できます。

```php
'state' => ['exists:states,abbreviation']
```

<!-- Occasionally, you may need to specify a specific database connection to be used for the `exists` query. You can accomplish this by prepending the connection name to the table name: -->
場合によっては、`exists` クエリに使用する特定のデータベース接続を指定する必要がある場合があります。これを行うには、テーブル名の前に接続名を追加します。

```php
'email' => ['exists:connection.staff,email']
```

<!-- Instead of specifying the table name directly, you may specify the Eloquent model which should be used to determine the table name: -->
テーブル名を直接指定する代わりに、テーブル名の決定に使用する Eloquent モデルを指定することもできます。

```php
'user_id' => ['exists:App\Models\User,id']
```

<!-- If you would like to customize the query executed by the validation rule, you may use the `Rule` class to fluently define the rule. -->
検証ルールによって実行されるクエリをカスタマイズしたい場合は、`Rule` クラスを使用してルールをスムーズに定義できます。

```php
use Illuminate\Database\Query\Builder;
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($data, [
    'email' => [
        'required',
        Rule::exists('staff')->where(function (Builder $query) {
            $query->where('account_id', 1);
        }),
    ],
]);
```

<!-- You may explicitly specify the database column name that should be used by the `exists` rule generated by the `Rule::exists` method by providing the column name as the second argument to the `exists` method: -->
`exists` メソッドの 2 番目の引数として列名を指定することで、`Rule::exists` メソッドによって生成される `exists` ルールで使用されるデータベース列名を明示的に指定できます。

```php
'state' => [Rule::exists('states', 'abbreviation')],
```

<!-- Sometimes, you may wish to validate whether an array of values exists in the database. You can do so by adding both the `exists` and [array](#rule-array) rules to the field being validated: -->
値の配列がデータベースに存在するかどうかを検証したい場合があります。これを行うには、検証対象のフィールドに `exists` ルールと [array](#rule-array) ルールの両方を追加します。

```php
'states' => ['array', Rule::exists('states', 'abbreviation')],
```

<!-- When both of these rules are assigned to a field, Laravel will automatically build a single query to determine if all of the given values exist in the specified table. -->
これらのルールの両方がフィールドに割り当てられている場合、Laravel は、指定されたすべての値が指定されたテーブルに存在するかどうかを判断する単一のクエリを自動的に構築します。

<a name="rule-extensions"></a>
<!-- #### extensions:_foo_,_bar_,... -->
#### extensions:_foo_,_bar_,...

<!-- The file under validation must have a user-assigned extension corresponding to one of the listed extensions: -->
検証中のファイルには、リストされた拡張子のいずれかに対応するユーザー割り当ての拡張子が必要です。

```php
'photo' => ['required', 'extensions:jpg,png'],
```

> [!WARNING]
> ユーザーが割り当てた拡張子のみによるファイルの検証に依存しないでください。通常、このルールは常に [mimes](#rule-mimes) ルールまたは [mimetypes](#rule-mimetypes) ルールと組み合わせて使用​​する必要があります。

<a name="rule-file"></a>
<!-- #### file -->
#### file

<!-- The field under validation must be a successfully uploaded file. -->
検証中のフィールドは、正常にアップロードされたファイルである必要があります。

<a name="rule-filled"></a>
<!-- #### filled -->
#### filled

<!-- The field under validation must not be empty when it is present. -->
検証中のフィールドが存在する場合、空であってはなりません。

<a name="rule-gt"></a>
<!-- #### gt:_field_ -->
#### gt:_field_

<!-- The field under validation must be greater than the given _field_ or _value_. The two fields must be of the same type. Strings, numerics, arrays, and files are evaluated using the same conventions as the [size](#rule-size) rule. -->
検証対象のフィールドは、指定された _field_ または _value_ より大きくなければなりません。 2 つのフィールドは同じタイプである必要があります。文字列、数値、配列、およびファイルは、[size](#rule-size) ルールと同じ規則を使用して評価されます。

<a name="rule-gte"></a>
<!-- #### gte:_field_ -->
#### gte:_field_

<!-- The field under validation must be greater than or equal to the given _field_ or _value_. The two fields must be of the same type. Strings, numerics, arrays, and files are evaluated using the same conventions as the [size](#rule-size) rule. -->
検証対象のフィールドは、指定された _field_ または _value_ 以上である必要があります。 2 つのフィールドは同じタイプである必要があります。文字列、数値、配列、およびファイルは、[size](#rule-size) ルールと同じ規則を使用して評価されます。

<a name="rule-hex-color"></a>
<!-- #### hex_color -->
#### hex_color

<!-- The field under validation must contain a valid color value in [hexadecimal](https://developer.mozilla.org/en-US/docs/Web/CSS/hex-color) format. -->
検証中のフィールドには、[hexadecimal](https://developer.mozilla.org/en-US/docs/Web/CSS/hex-color) 形式の有効な色の値が含まれている必要があります。

<a name="rule-image"></a>
<!-- #### image -->
#### image

<!-- The file under validation must be an image (jpg, jpeg, png, bmp, gif, or webp). -->
検証対象のファイルは画像 (jpg、jpeg、png、bmp、gif、または webp) である必要があります。

> [!WARNING]
> デフォルトでは、XSS 脆弱性の可能性があるため、画像ルールは SVG ファイルを許可しません。 SVG ファイルを許可する必要がある場合は、`allow_svg` ディレクティブを `image` ルール (`image:allow_svg`) に指定できます。

<a name="rule-in"></a>
<!-- #### in:_foo_,_bar_,... -->
#### in:_foo_,_bar_,...

<!-- The field under validation must be included in the given list of values. Since this rule often requires you to `implode` an array, the `Rule::in` method may be used to fluently construct the rule: -->
検証中のフィールドは、指定された値のリストに含まれている必要があります。このルールでは配列を `implode` する必要があることが多いため、ルールをスムーズに構築するために `Rule::in` メソッドを使用できます。

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($data, [
    'zones' => [
        'required',
        Rule::in(['first-zone', 'second-zone']),
    ],
]);
```

<!-- When the `in` rule is combined with the `array` rule, each value in the input array must be present within the list of values provided to the `in` rule. In the following example, the `LAS` airport code in the input array is invalid since it is not contained in the list of airports provided to the `in` rule: -->
`in` ルールを `array` ルールと組み合わせる場合、入力配列の各値は、`in` ルールに提供される値のリスト内に存在する必要があります。次の例では、入力配列の `LAS` 空港コードは、`in` ルールに指定された空港のリストに含まれていないため、無効です。

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

$input = [
    'airports' => ['NYC', 'LAS'],
];

Validator::make($input, [
    'airports' => [
        'required',
        'array',
    ],
    'airports.*' => Rule::in(['NYC', 'LIT']),
]);
```

<a name="rule-in-array"></a>
<!-- #### in_array:_anotherfield_.* -->
#### in_array:_anotherfield_.*

<!-- The field under validation must exist in _anotherfield_'s values. -->
検証中のフィールドは、_anotherfield_ の値に存在する必要があります。

<a name="rule-in-array-keys"></a>
<!-- #### in_array_keys:_value_.* -->
#### in_array_keys:_value_.*

<!-- The field under validation must be an array having at least one of the given _values_ as a key within the array: -->
検証対象のフィールドは、配列内のキーとして指定された _values_ の少なくとも 1 つを持つ配列である必要があります。

```php
'config' => ['array', 'in_array_keys:timezone']
```

<a name="rule-integer"></a>
<!-- #### integer -->
#### integer

<!-- The field under validation must be an integer. -->
検証対象のフィールドは整数である必要があります。

<!-- You may use the `strict` parameter to only consider the field valid if its type is `integer`. Strings with integer values will be considered invalid: -->
`strict` パラメーターを使用すると、フィールドのタイプが `integer` の場合にのみフィールドが有効であると見なすことができます。整数値を含む文字列は無効とみなされます。

```php
'age' => ['integer:strict']
```

> [!WARNING]
> この検証ルールは、入力が「整数」変数タイプであることを検証するのではなく、入力が PHP の `FILTER_VALIDATE_INT` ルールで受け入れられるタイプであることのみを検証します。入力が数値であることを検証する必要がある場合は、このルールを [the `numeric` validation rule](#rule-numeric) と組み合わせて使用​​してください。

<a name="rule-ip"></a>
<!-- #### ip -->
#### ip

<!-- The field under validation must be an IP address. -->
検証対象のフィールドは IP アドレスである必要があります。

<a name="ipv4"></a>
<!-- #### ipv4 -->
#### ipv4

<!-- The field under validation must be an IPv4 address. -->
検証対象のフィールドは IPv4 アドレスである必要があります。

<a name="ipv6"></a>
<!-- #### ipv6 -->
#### ipv6

<!-- The field under validation must be an IPv6 address. -->
検証対象のフィールドは IPv6 アドレスである必要があります。

<a name="rule-json"></a>
<!-- #### json -->
#### json

<!-- The field under validation must be a valid JSON string. -->
検証対象のフィールドは有効な JSON 文字列である必要があります。

<a name="rule-lt"></a>
<!-- #### lt:_field_ -->
#### lt:_field_

<!-- The field under validation must be less than the given _field_. The two fields must be of the same type. Strings, numerics, arrays, and files are evaluated using the same conventions as the [size](#rule-size) rule. -->
検証対象のフィールドは、指定された _field_ より小さくなければなりません。 2 つのフィールドは同じタイプである必要があります。文字列、数値、配列、およびファイルは、[size](#rule-size) ルールと同じ規則を使用して評価されます。

<a name="rule-lte"></a>
<!-- #### lte:_field_ -->
#### lte:_field_

<!-- The field under validation must be less than or equal to the given _field_. The two fields must be of the same type. Strings, numerics, arrays, and files are evaluated using the same conventions as the [size](#rule-size) rule. -->
検証対象のフィールドは、指定された _field_ 以下である必要があります。 2 つのフィールドは同じタイプである必要があります。文字列、数値、配列、およびファイルは、[size](#rule-size) ルールと同じ規則を使用して評価されます。

<a name="rule-lowercase"></a>
<!-- #### lowercase -->
#### lowercase

<!-- The field under validation must be lowercase. -->
検証中のフィールドは小文字である必要があります。

<a name="rule-list"></a>
<!-- #### list -->
#### list

<!-- The field under validation must be an array that is a list. An array is considered a list if its keys consist of consecutive numbers from 0 to `count($array) - 1`. -->
検証対象のフィールドはリストである配列である必要があります。キーが 0 から `count($array) - 1` までの連続した数字で構成されている場合、配列はリストとみなされます。

<a name="rule-mac"></a>
<!-- #### mac_address -->
#### mac_address

<!-- The field under validation must be a MAC address. -->
検証対象のフィールドは MAC アドレスである必要があります。

<a name="rule-max"></a>
<!-- #### max:_value_ -->
#### max:_value_

<!-- The field under validation must be less than or equal to a maximum _value_. Strings, numerics, arrays, and files are evaluated in the same fashion as the [size](#rule-size) rule. -->
検証対象のフィールドは、最大 _value_ 以下である必要があります。文字列、数値、配列、ファイルは、[size](#rule-size) ルールと同じ方法で評価されます。

<a name="rule-max-digits"></a>
<!-- #### max_digits:_value_ -->
#### max_digits:_value_

<!-- The integer under validation must have a maximum length of _value_. -->
検証される整数の最大長は _value_ である必要があります。

<a name="rule-mimetypes"></a>
<!-- #### mimetypes:_text/plain_,... -->
#### mimetypes:_text/plain_,...

<!-- The file under validation must match one of the given MIME types: -->
検証中のファイルは、指定された MIME タイプのいずれかに一致する必要があります。

```php
'video' => ['mimetypes:video/avi,video/mpeg,video/quicktime'],

'media' => ['mimetypes:image/*,video/*'],
```

<!-- To determine the MIME type of the uploaded file, the file's contents will be read and the framework will attempt to guess the MIME type, which may be different from the client's provided MIME type. -->
アップロードされたファイルの MIME タイプを判断するために、ファイルの内容が読み取られ、フレームワークは MIME タイプを推測しようとしますが、これはクライアントが提供した MIME タイプとは異なる場合があります。

<a name="rule-mimes"></a>
<!-- #### mimes:_foo_,_bar_,... -->
#### mimes:_foo_,_bar_,...

<!-- The file under validation must have a MIME type corresponding to one of the listed extensions: -->
検証中のファイルには、リストされた拡張子のいずれかに対応する MIME タイプが必要です。

```php
'photo' => ['mimes:jpg,bmp,png']
```

<!-- Even though you only need to specify the extensions, this rule actually validates the MIME type of the file by reading the file's contents and guessing its MIME type. A full listing of MIME types and their corresponding extensions may be found at the following location: -->
拡張子を指定するだけで済みますが、このルールは実際には、ファイルの内容を読み取り、その MIME タイプを推測することによってファイルの MIME タイプを検証します。 MIME タイプとそれに対応する拡張子の完全なリストは、次の場所にあります。

<!-- [https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types](https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types) -->
[https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types](https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types)

<a name="mime-types-and-extensions"></a>
<!-- #### MIME Types and Extensions -->
#### MIME Types and Extensions

<!-- This validation rule does not verify agreement between the MIME type and the extension the user assigned to the file. For example, the `mimes:png` validation rule would consider a file containing valid PNG content to be a valid PNG image, even if the file is named `photo.txt`. If you would like to validate the user-assigned extension of the file, you may use the [extensions](#rule-extensions) rule. -->
この検証ルールは、MIME タイプとユーザーがファイルに割り当てた拡張子との間の一致を検証しません。たとえば、`mimes:png` 検証ルールでは、ファイルの名前が `photo.txt` であっても、有効な PNG コンテンツを含むファイルは有効な PNG イメージであると見なされます。ユーザーが割り当てたファイルの拡張子を検証したい場合は、[extensions](#rule-extensions) ルールを使用できます。

<a name="rule-min"></a>
<!-- #### min:_value_ -->
#### min:_value_

<!-- The field under validation must have a minimum _value_. Strings, numerics, arrays, and files are evaluated in the same fashion as the [size](#rule-size) rule. -->
検証中のフィールドには最小の _value_ が必要です。文字列、数値、配列、ファイルは、[size](#rule-size) ルールと同じ方法で評価されます。

<a name="rule-min-digits"></a>
<!-- #### min_digits:_value_ -->
#### min_digits:_value_

<!-- The integer under validation must have a minimum length of _value_. -->
検証される整数には、_value_ の最小長が必要です。

<a name="rule-multiple-of"></a>
<!-- #### multiple_of:_value_ -->
#### multiple_of:_value_

<!-- The field under validation must be a multiple of _value_. -->
検証対象のフィールドは、_value_ の倍数である必要があります。

<a name="rule-missing"></a>
<!-- #### missing -->
#### missing

<!-- The field under validation must not be present in the input data. -->
検証中のフィールドは入力データに存在してはなりません。

<a name="rule-missing-if"></a>
<!-- #### missing_if:_anotherfield_,_value_,... -->
#### missing_if:_anotherfield_,_value_,...

<!-- The field under validation must not be present if the _anotherfield_ field is equal to any _value_. -->
_anotherfield_ フィールドがいずれかの _value_ と等しい場合、検証中のフィールドは存在してはなりません。

<a name="rule-missing-unless"></a>
<!-- #### missing_unless:_anotherfield_,_value_ -->
#### missing_unless:_anotherfield_,_value_

<!-- The field under validation must not be present unless the _anotherfield_ field is equal to any _value_. -->
_anotherfield_ フィールドがいずれかの _value_ と等しくない限り、検証中のフィールドは存在してはなりません。

<a name="rule-missing-with"></a>
<!-- #### missing_with:_foo_,_bar_,... -->
#### missing_with:_foo_,_bar_,...

<!-- The field under validation must not be present _only if_ any of the other specified fields are present. -->
検証中のフィールドは、他の指定されたフィールドが存在する場合にのみ存在してはなりません。

<a name="rule-missing-with-all"></a>
<!-- #### missing_with_all:_foo_,_bar_,... -->
#### missing_with_all:_foo_,_bar_,...

<!-- The field under validation must not be present _only if_ all of the other specified fields are present. -->
検証中のフィールドは、他の指定されたフィールドがすべて存在する場合にのみ存在してはなりません。

<a name="rule-not-in"></a>
<!-- #### not_in:_foo_,_bar_,... -->
#### not_in:_foo_,_bar_,...

<!-- The field under validation must not be included in the given list of values. The `Rule::notIn` method may be used to fluently construct the rule: -->
検証中のフィールドは、指定された値のリストに含めてはなりません。 `Rule::notIn` メソッドを使用すると、ルールをスムーズに構築できます。

```php
use Illuminate\Validation\Rule;

Validator::make($data, [
    'toppings' => [
        'required',
        Rule::notIn(['sprinkles', 'cherries']),
    ],
]);
```

<a name="rule-not-regex"></a>
<!-- #### not_regex:_pattern_ -->
#### not_regex:_pattern_

<!-- The field under validation must not match the given regular expression. -->
検証中のフィールドは、指定された正規表現と一致してはなりません。

<!-- Internally, this rule uses the PHP `preg_match` function. The pattern specified should obey the same formatting required by `preg_match` and thus also include valid delimiters. For example: `'email' => ['not_regex:/^.+$/i']`. -->
内部的には、このルールは PHP `preg_match` 関数を使用します。指定されたパターンは、`preg_match` で必要とされるのと同じ形式に従っており、有効な区切り文字も含まれている必要があります。例: `'email' => ['not_regex:/^.+$/i']`。

<a name="rule-nullable"></a>
<!-- #### nullable -->
#### nullable

<!-- The field under validation may be `null`. -->
検証中のフィールドは `null` である可能性があります。

<a name="rule-numeric"></a>
<!-- #### numeric -->
#### numeric

<!-- The field under validation must be [numeric](https://www.php.net/manual/en/function.is-numeric.php). -->
検証対象のフィールドは [numeric](https://www.php.net/manual/en/function.is-numeric.php) である必要があります。

<!-- You may use the `strict` parameter to only consider the field valid if its value is an integer or float type. Numeric strings will be considered invalid: -->
`strict` パラメータを使用すると、値が整数型または浮動小数点型の場合にのみフィールドが有効であると見なすことができます。数値文字列は無効とみなされます。

```php
'amount' => ['numeric:strict']
```

<a name="rule-present"></a>
<!-- #### present -->
#### present

<!-- The field under validation must exist in the input data. -->
検証対象のフィールドは入力データに存在する必要があります。

<a name="rule-present-if"></a>
<!-- #### present_if:_anotherfield_,_value_,... -->
#### present_if:_anotherfield_,_value_,...

<!-- The field under validation must be present if the _anotherfield_ field is equal to any _value_. -->
_anotherfield_ フィールドがいずれかの _value_ と等しい場合、検証中のフィールドが存在する必要があります。

<a name="rule-present-unless"></a>
<!-- #### present_unless:_anotherfield_,_value_ -->
#### present_unless:_anotherfield_,_value_

<!-- The field under validation must be present unless the _anotherfield_ field is equal to any _value_. -->
_anotherfield_ フィールドがいずれかの _value_ と等しくない限り、検証対象のフィールドが存在する必要があります。

<a name="rule-present-with"></a>
<!-- #### present_with:_foo_,_bar_,... -->
#### present_with:_foo_,_bar_,...

<!-- The field under validation must be present _only if_ any of the other specified fields are present. -->
検証中のフィールドは、他の指定されたフィールドのいずれかが存在する場合にのみ存在する必要があります。

<a name="rule-present-with-all"></a>
<!-- #### present_with_all:_foo_,_bar_,... -->
#### present_with_all:_foo_,_bar_,...

<!-- The field under validation must be present _only if_ all of the other specified fields are present. -->
検証中のフィールドは、他の指定されたフィールドがすべて存在する場合にのみ存在する必要があります。

<a name="rule-prohibited"></a>
<!-- #### prohibited -->
#### prohibited

<!-- The field under validation must be missing or empty. A field is "empty" if it meets one of the following criteria: -->
検証中のフィールドは欠落しているか空である必要があります。次の基準のいずれかを満たしている場合、フィールドは「空」です。

<div class="content-list" markdown="1">

<!-- - The value is `null`. - The value is an empty string. - The value is an empty array or empty `Countable` object. - The value is an uploaded file with an empty path. -->
- 値は `null` です。
- 値は空の文字列です。
- 値は空の配列または空の `Countable` オブジェクトです。
- 値は、空のパスを持つアップロードされたファイルです。

</div>

<a name="rule-prohibited-if"></a>
<!-- #### prohibited_if:_anotherfield_,_value_,... -->
#### prohibited_if:_anotherfield_,_value_,...

<!-- The field under validation must be missing or empty if the _anotherfield_ field is equal to any _value_. A field is "empty" if it meets one of the following criteria: -->
_anotherfield_ フィールドがいずれかの _value_ と等しい場合、検証対象のフィールドは欠落しているか空である必要があります。次の基準のいずれかを満たしている場合、フィールドは「空」です。

<div class="content-list" markdown="1">

<!-- - The value is `null`. - The value is an empty string. - The value is an empty array or empty `Countable` object. - The value is an uploaded file with an empty path. -->
- 値は `null` です。
- 値は空の文字列です。
- 値は空の配列または空の `Countable` オブジェクトです。
- 値は、空のパスを持つアップロードされたファイルです。

</div>

<!-- If complex conditional prohibition logic is required, you may utilize the `Rule::prohibitedIf` method. This method accepts a boolean or a closure. When given a closure, the closure should return `true` or `false` to indicate if the field under validation should be prohibited: -->
複雑な条件付き禁止ロジックが必要な場合は、`Rule::prohibitedIf` メソッドを利用できます。このメソッドはブール値またはクロージャを受け入れます。クロージャが指定された場合、クロージャは `true` または `false` を返し、検証中のフィールドを禁止する必要があるかどうかを示す必要があります。

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($request->all(), [
    'role_id' => [Rule::prohibitedIf($request->user()->is_admin)],
]);

Validator::make($request->all(), [
    'role_id' => [Rule::prohibitedIf(fn () => $request->user()->is_admin)],
]);
```
<a name="rule-prohibited-if-accepted"></a>
<!-- #### prohibited_if_accepted:_anotherfield_,... -->
#### prohibited_if_accepted:_anotherfield_,...

<!-- The field under validation must be missing or empty if the _anotherfield_ field is equal to `"yes"`, `"on"`, `1`, `"1"`, `true`, or `"true"`. -->
_anotherfield_ フィールドが `"yes"`、`"on"`、`1`、`"1"`、`true`、または `"true"` と等しい場合、検証中のフィールドは欠落しているか空である必要があります。

<a name="rule-prohibited-if-declined"></a>
<!-- #### prohibited_if_declined:_anotherfield_,... -->
#### prohibited_if_declined:_anotherfield_,...

<!-- The field under validation must be missing or empty if the _anotherfield_ field is equal to `"no"`, `"off"`, `0`, `"0"`, `false`, or `"false"`. -->
_anotherfield_ フィールドが `"no"`、`"off"`、`0`、`"0"`、`false`、または `"false"` と等しい場合、検証中のフィールドは欠落しているか空である必要があります。

<a name="rule-prohibited-unless"></a>
<!-- #### prohibited_unless:_anotherfield_,_value_,... -->
#### prohibited_unless:_anotherfield_,_value_,...

<!-- The field under validation must be missing or empty unless the _anotherfield_ field is equal to any _value_. A field is "empty" if it meets one of the following criteria: -->
_anotherfield_ フィールドがいずれかの _value_ と等しい場合を除き、検証対象のフィールドは欠落しているか空である必要があります。次の基準のいずれかを満たしている場合、フィールドは「空」です。

<div class="content-list" markdown="1">

<!-- - The value is `null`. - The value is an empty string. - The value is an empty array or empty `Countable` object. - The value is an uploaded file with an empty path. -->
- 値は `null` です。
- 値は空の文字列です。
- 値は空の配列または空の `Countable` オブジェクトです。
- 値は、空のパスを持つアップロードされたファイルです。

</div>

<!-- If complex conditional prohibition logic is required, you may utilize the `Rule::prohibitedUnless` method. This method accepts a boolean or a closure. When given a closure, the closure should return `true` or `false` to indicate if the field under validation should not be prohibited: -->
複雑な条件付き禁止ロジックが必要な場合は、`Rule::prohibitedUnless` メソッドを利用できます。このメソッドはブール値またはクロージャを受け入れます。クロージャが指定された場合、クロージャは `true` または `false` を返し、検証中のフィールドを禁止すべきかどうかを示す必要があります。

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($request->all(), [
    'role_id' => [Rule::prohibitedUnless($request->user()->is_admin)],
]);

Validator::make($request->all(), [
    'role_id' => [Rule::prohibitedUnless(fn () => $request->user()->is_admin)],
]);
```

<a name="rule-prohibits"></a>
<!-- #### prohibits:_anotherfield_,... -->
#### prohibits:_anotherfield_,...

<!-- If the field under validation is not missing or empty, all fields in _anotherfield_ must be missing or empty. A field is "empty" if it meets one of the following criteria: -->
検証中のフィールドが欠落または空でない場合、_anotherfield_ のすべてのフィールドが欠落または空である必要があります。次の基準のいずれかを満たしている場合、フィールドは「空」です。

<div class="content-list" markdown="1">

<!-- - The value is `null`. - The value is an empty string. - The value is an empty array or empty `Countable` object. - The value is an uploaded file with an empty path. -->
- 値は `null` です。
- 値は空の文字列です。
- 値は空の配列または空の `Countable` オブジェクトです。
- 値は、空のパスを持つアップロードされたファイルです。

</div>

<a name="rule-regex"></a>
<!-- #### regex:_pattern_ -->
#### regex:_pattern_

<!-- The field under validation must match the given regular expression. -->
検証中のフィールドは、指定された正規表現と一致する必要があります。

<!-- Internally, this rule uses the PHP `preg_match` function. The pattern specified should obey the same formatting required by `preg_match` and thus also include valid delimiters. For example: `'email' => ['regex:/^.+@.+$/i']`. -->
内部的には、このルールは PHP `preg_match` 関数を使用します。指定されたパターンは、`preg_match` で必要とされるのと同じ形式に従っており、有効な区切り文字も含まれている必要があります。例: `'email' => ['regex:/^.+@.+$/i']`。

<a name="rule-required"></a>
<!-- #### required -->
#### required

<!-- The field under validation must be present in the input data and not empty. A field is "empty" if it meets one of the following criteria: -->
検証対象のフィールドは入力データに存在する必要があり、空であってはなりません。次の基準のいずれかを満たしている場合、フィールドは「空」です。

<div class="content-list" markdown="1">

<!-- - The value is `null`. - The value is an empty string. - The value is an empty array or empty `Countable` object. - The value is an uploaded file with no path. -->
- 値は `null` です。
- 値は空の文字列です。
- 値は空の配列または空の `Countable` オブジェクトです。
- 値は、パスのないアップロードされたファイルです。

</div>

<a name="rule-required-if"></a>
<!-- #### required_if:_anotherfield_,_value_,... -->
#### required_if:_anotherfield_,_value_,...

<!-- The field under validation must be present and not empty if the _anotherfield_ field is equal to any _value_. -->
_anotherfield_ フィールドがいずれかの _value_ と等しい場合、検証中のフィールドは存在する必要があり、空であってはなりません。

<!-- If you would like to construct a more complex condition for the `required_if` rule, you may use the `Rule::requiredIf` method. This method accepts a boolean or a closure. When passed a closure, the closure should return `true` or `false` to indicate if the field under validation is required: -->
`required_if` ルールのより複雑な条件を作成したい場合は、`Rule::requiredIf` メソッドを使用できます。このメソッドはブール値またはクロージャを受け入れます。クロージャが渡されると、クロージャは `true` または `false` を返し、検証中のフィールドが必要かどうかを示す必要があります。

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($request->all(), [
    'role_id' => [Rule::requiredIf($request->user()->is_admin)],
]);

Validator::make($request->all(), [
    'role_id' => [Rule::requiredIf(fn () => $request->user()->is_admin)],
]);
```

<a name="rule-required-if-accepted"></a>
<!-- #### required_if_accepted:_anotherfield_,... -->
#### required_if_accepted:_anotherfield_,...

<!-- The field under validation must be present and not empty if the _anotherfield_ field is equal to `"yes"`, `"on"`, `1`, `"1"`, `true`, or `"true"`. -->
_anotherfield_ フィールドが `"yes"`、`"on"`、`1`、`"1"`、`true`、または `"true"` と等しい場合、検証対象のフィールドが存在し、空であってはなりません。

<a name="rule-required-if-declined"></a>
<!-- #### required_if_declined:_anotherfield_,... -->
#### required_if_declined:_anotherfield_,...

<!-- The field under validation must be present and not empty if the _anotherfield_ field is equal to `"no"`, `"off"`, `0`, `"0"`, `false`, or `"false"`. -->
_anotherfield_ フィールドが `"no"`、`"off"`、`0`、`"0"`、`false`、または `"false"` と等しい場合、検証対象のフィールドが存在し、空であってはなりません。

<a name="rule-required-unless"></a>
<!-- #### required_unless:_anotherfield_,_value_,... -->
#### required_unless:_anotherfield_,_value_,...

<!-- The field under validation must be present and not empty unless the _anotherfield_ field is equal to any _value_. This also means _anotherfield_ must be present in the request data unless _value_ is `null`. If _value_ is `null` (`required_unless:name,null`), the field under validation will be required unless the comparison field is `null` or the comparison field is missing from the request data. -->
検証中のフィールドは存在する必要があり、_anotherfield_ フィールドがいずれかの _value_ と等しい場合を除き、空であってはなりません。これは、_value_ が `null` でない限り、_anotherfield_ がリクエスト データに存在する必要があることも意味します。 _value_ が `null` (`required_unless:name,null`) の場合、比較フィールドが `null` でない限り、または比較フィールドがリクエスト データに欠落している場合を除き、検証対象のフィールドが必要になります。

<!-- If you would like to construct a more complex condition for the `required_unless` rule, you may use the `Rule::requiredUnless` method. This method accepts a boolean or a closure. When passed a closure, the closure should return `true` or `false` to indicate if the field under validation is not required: -->
`required_unless` ルールのより複雑な条件を作成したい場合は、`Rule::requiredUnless` メソッドを使用できます。このメソッドはブール値またはクロージャを受け入れます。クロージャが渡されると、クロージャは `true` または `false` を返して、検証中のフィールドが不要かどうかを示す必要があります。

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($request->all(), [
    'role_id' => [Rule::requiredUnless($request->user()->is_admin)],
]);

Validator::make($request->all(), [
    'role_id' => [Rule::requiredUnless(fn () => $request->user()->is_admin)],
]);
```

<a name="rule-required-with"></a>
<!-- #### required_with:_foo_,_bar_,... -->
#### required_with:_foo_,_bar_,...

<!-- The field under validation must be present and not empty _only if_ any of the other specified fields are present and not empty. -->
検証対象のフィールドは、他の指定されたフィールドが存在し、空でない場合にのみ、存在し、空であってはなりません。

<a name="rule-required-with-all"></a>
<!-- #### required_with_all:_foo_,_bar_,... -->
#### required_with_all:_foo_,_bar_,...

<!-- The field under validation must be present and not empty _only if_ all of the other specified fields are present and not empty. -->
検証対象のフィールドは、他の指定されたフィールドがすべて存在し、空でない場合にのみ、存在し、空であってはなりません。

<a name="rule-required-without"></a>
<!-- #### required_without:_foo_,_bar_,... -->
#### required_without:_foo_,_bar_,...

<!-- The field under validation must be present and not empty _only when_ any of the other specified fields are empty or not present. -->
検証対象のフィールドは、指定された他のフィールドが空であるか存在しない場合にのみ、空ではなく存在する必要があります。

<a name="rule-required-without-all"></a>
<!-- #### required_without_all:_foo_,_bar_,... -->
#### required_without_all:_foo_,_bar_,...

<!-- The field under validation must be present and not empty _only when_ all of the other specified fields are empty or not present. -->
検証対象のフィールドは、他の指定フィールドがすべて空であるか存在しない場合にのみ、空ではなく存在する必要があります。

<a name="rule-required-array-keys"></a>
<!-- #### required_array_keys:_foo_,_bar_,... -->
#### required_array_keys:_foo_,_bar_,...

<!-- The field under validation must be an array and must contain at least the specified keys. -->
検証対象のフィールドは配列である必要があり、少なくとも指定されたキーが含まれている必要があります。

<a name="rule-same"></a>
<!-- #### same:_field_ -->
#### same:_field_

<!-- The given _field_ must match the field under validation. -->
指定された _field_ は検証中のフィールドと一致する必要があります。

<a name="rule-size"></a>
<!-- #### size:_value_ -->
#### size:_value_

<!-- The field under validation must have a size matching the given _value_. For string data, _value_ corresponds to the number of characters. For numeric data, _value_ corresponds to a given integer value (the attribute must also have the `numeric` or `integer` rule). For an array, _size_ corresponds to the `count` of the array. For files, _size_ corresponds to the file size in kilobytes. Let's look at some examples: -->
検証中のフィールドのサイズは、指定された _value_ と一致する必要があります。文字列データの場合、_value_ は文字数に対応します。数値データの場合、_value_ は指定された整数値に対応します (属性には `numeric` または `integer` ルールも必要です)。配列の場合、_size_ は配列の `count` に対応します。ファイルの場合、_size_ はキロバイト単位のファイル サイズに対応します。いくつかの例を見てみましょう。

```php
// Validate that a string is exactly 12 characters long...
'title' => ['size:12'];

// Validate that a provided integer equals 10...
'seats' => ['integer', 'size:10'];

// Validate that an array has exactly 5 elements...
'tags' => ['array', 'size:5'];

// Validate that an uploaded file is exactly 512 kilobytes...
'image' => ['file', 'size:512'];
```

<a name="rule-starts-with"></a>
<!-- #### starts_with:_foo_,_bar_,... -->
#### starts_with:_foo_,_bar_,...

<!-- The field under validation must start with one of the given values. -->
検証中のフィールドは、指定された値のいずれかで始まる必要があります。

<a name="rule-string"></a>
<!-- #### string -->
#### string

<!-- The field under validation must be a string. If you would like to allow the field to also be `null`, you should assign the `nullable` rule to the field. -->
検証対象のフィールドは文字列である必要があります。フィールドを `null` にすることも許可したい場合は、フィールドに `nullable` ルールを割り当てる必要があります。

<!-- For convenience, string validation rules may also be constructed using the fluent `Rule::string()` rule builder: -->
便宜上、文字列検証ルールは、滑らかな `Rule::string()` ルール ビルダを使用して構築することもできます。

```php
use Illuminate\Validation\Rule;

'title' => [
    'required',
    Rule::string()
        ->min(3)
        ->max(255)
        ->alphaDash(ascii: true),
],
```

<!-- The string rule builder provides methods for common string constraints, including `alpha`, `alphaDash`, `alphaNumeric`, `ascii`, `between`, `doesntEndWith`, `doesntStartWith`, `endsWith`, `exactly`, `lowercase`, `max`, `min`, `startsWith`, and `uppercase`. Since the rule builder is conditionable, you may also use the `when` and `unless` methods to conditionally apply constraints. -->
文字列ルール ビルダは、`alpha`、`alphaDash`、`alphaNumeric`、`ascii`、`between`、`doesntEndWith`、`doesntStartWith`、`endsWith`、`exactly` などの一般的な文字列制約のメソッドを提供します。 `lowercase`、`max`、`min`、`startsWith`、および `uppercase`。ルール ビルダは条件付きであるため、`when` メソッドと `unless` メソッドを使用して条件付きで制約を適用することもできます。

<a name="rule-timezone"></a>
<!-- #### timezone -->
#### timezone

<!-- The field under validation must be a valid timezone identifier according to the `DateTimeZone::listIdentifiers` method. -->
検証対象のフィールドは、`DateTimeZone::listIdentifiers` メソッドに従った有効なタイムゾーン識別子である必要があります。

<!-- The arguments [accepted by the `DateTimeZone::listIdentifiers` method](https://www.php.net/manual/en/datetimezone.listidentifiers.php) may also be provided to this validation rule: -->
引数 [accepted by the `DateTimeZone::listIdentifiers` method](https://www.php.net/manual/en/datetimezone.listidentifiers.php) もこの検証ルールに指定できます。

```php
'timezone' => ['required', 'timezone:all'];

'timezone' => ['required', 'timezone:Africa'];

'timezone' => ['required', 'timezone:per_country,US'];
```

<a name="rule-unique"></a>
<!-- #### unique:_table_,_column_ -->
#### unique:_table_,_column_

<!-- The field under validation must not exist within the given database table. -->
検証中のフィールドは、指定されたデータベース テーブル内に存在してはなりません。

<!-- **Specifying a Custom Table / Column Name:** -->
**カスタム テーブル/列名の指定:**

<!-- Instead of specifying the table name directly, you may specify the Eloquent model which should be used to determine the table name: -->
テーブル名を直接指定する代わりに、テーブル名の決定に使用する Eloquent モデルを指定することもできます。

```php
'email' => ['unique:App\Models\User,email_address']
```

<!-- The `column` option may be used to specify the field's corresponding database column. If the `column` option is not specified, the name of the field under validation will be used. -->
`column` オプションを使用して、フィールドに対応するデータベース列を指定できます。 `column` オプションが指定されていない場合は、検証中のフィールドの名前が使用されます。

```php
'email' => ['unique:users,email_address']
```

<!-- **Specifying a Custom Database Connection** -->
**カスタム データベース接続の指定**

<!-- Occasionally, you may need to set a custom connection for database queries made by the Validator. To accomplish this, you may prepend the connection name to the table name: -->
場合によっては、バリデーターによって行われるデータベース クエリに対してカスタム接続を設定する必要がある場合があります。これを実現するには、テーブル名の前に接続名を追加します。

```php
'email' => ['unique:connection.users,email_address']
```

<!-- **Forcing a Unique Rule to Ignore a Given ID:** -->
**特定の ID を無視するように固有のルールを強制する:**

<!-- Sometimes, you may wish to ignore a given ID during unique validation. For example, consider an "update profile" screen that includes the user's name, email address, and location. You will probably want to verify that the email address is unique. However, if the user only changes the name field and not the email field, you do not want a validation error to be thrown because the user is already the owner of the email address in question. -->
場合によっては、一意の検証中に特定の ID を無視したい場合があります。たとえば、ユーザーの名前、電子メール アドレス、場所が含まれる「プロフィールの更新」画面を考えてみましょう。おそらく、電子メール アドレスが一意であることを確認する必要があるでしょう。ただし、ユーザーが名前フィールドのみを変更し、電子メール フィールドを変更しない場合、ユーザーはすでに問題の電子メール アドレスの所有者であるため、検証エラーがスローされることは望ましくありません。

<!-- To instruct the validator to ignore the user's ID, we'll use the `Rule` class to fluently define the rule. -->
ユーザーの ID を無視するようにバリデーターに指示するには、`Rule` クラスを使用してルールをスムーズに定義します。

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($data, [
    'email' => [
        'required',
        Rule::unique('users')->ignore($user->id),
    ],
]);
```

> [!WARNING]
> ユーザー制御のリクエスト入力を `ignore` メソッドに渡さないでください。代わりに、Eloquent モデル インスタンスからの自動インクリメント ID や UUID など、システムが生成した一意の ID のみを渡す必要があります。そうしないと、アプリケーションが SQL インジェクション攻撃に対して脆弱になります。

<!-- Instead of passing the model key's value to the `ignore` method, you may also pass the entire model instance. Laravel will automatically extract the key from the model: -->
モデル キーの値を `ignore` メソッドに渡す代わりに、モデル インスタンス全体を渡すこともできます。 Laravel はモデルからキーを自動的に抽出します。

```php
Rule::unique('users')->ignore($user)
```

<!-- If your table uses a primary key column name other than `id`, you may specify the name of the column when calling the `ignore` method: -->
テーブルで `id` 以外の主キー列名を使用する場合は、`ignore` メソッドを呼び出すときに列の名前を指定できます。

```php
Rule::unique('users')->ignore($user->id, 'user_id')
```

<!-- By default, the `unique` rule will check the uniqueness of the column matching the name of the attribute being validated. However, you may pass a different column name as the second argument to the `unique` method: -->
デフォルトでは、`unique` ルールは、検証される属性の名前に一致する列の一意性をチェックします。ただし、別の列名を `unique` メソッドの 2 番目の引数として渡すこともできます。

```php
Rule::unique('users', 'email_address')->ignore($user->id)
```

<!-- **Adding Additional Where Clauses:** -->
**Where 句を追加する:**

<!-- You may specify additional query conditions by customizing the query using the `where` method. For example, let's add a query condition that scopes the query to only search records that have an `account_id` column value of `1`: -->
`where` メソッドを使用してクエリをカスタマイズすることにより、追加のクエリ条件を指定できます。たとえば、`account_id` 列の値が `1` であるレコードのみを検索するようにクエリの範囲を設定するクエリ条件を追加してみましょう。

```php
'email' => Rule::unique('users')->where(fn (Builder $query) => $query->where('account_id', 1))
```

<!-- **Ignoring Soft Deleted Records in Unique Checks:** -->
**一意のチェックで論理的に削除されたレコードを無視する:**

<!-- By default, the unique rule includes soft deleted records when determining uniqueness. To exclude soft deleted records from the uniqueness check, you may invoke the `withoutTrashed` method: -->
デフォルトでは、一意性を判断するときに、一意のルールには論理的に削除されたレコードが含まれます。論理的に削除されたレコードを一意性チェックから除外するには、`withoutTrashed` メソッドを呼び出すことができます。

```php
Rule::unique('users')->withoutTrashed();
```

<!-- If your model uses a column name other than `deleted_at` for soft deleted records, you may provide the column name when invoking the `withoutTrashed` method: -->
モデルで論理的に削除されたレコードに `deleted_at` 以外の列名を使用する場合は、`withoutTrashed` メソッドを呼び出すときに列名を指定できます。

```php
Rule::unique('users')->withoutTrashed('was_deleted_at');
```

<a name="rule-uppercase"></a>
<!-- #### uppercase -->
#### uppercase

<!-- The field under validation must be uppercase. -->
検証中のフィールドは大文字である必要があります。

<a name="rule-url"></a>
<!-- #### url -->
#### url

<!-- The field under validation must be a valid URL. -->
検証対象のフィールドは有効な URL である必要があります。

<!-- If you would like to specify the URL protocols that should be considered valid, you may pass the protocols as validation rule parameters: -->
有効であるとみなされる URL プロトコルを指定したい場合は、プロトコルを検証ルール パラメーターとして渡すことができます。

```php
'url' => ['url:http,https'],

'game' => ['url:minecraft,steam'],
```

<a name="rule-ulid"></a>
<!-- #### ulid -->
#### ulid

<!-- The field under validation must be a valid [Universally Unique Lexicographically Sortable Identifier](https://github.com/ulid/spec) (ULID). -->
検証対象のフィールドは有効な [Universally Unique Lexicographically Sortable Identifier](https://github.com/ulid/spec) (ULID) である必要があります。

<a name="rule-uuid"></a>
<!-- #### uuid -->
#### uuid

<!-- The field under validation must be a valid RFC 9562 (version 1, 3, 4, 5, 6, 7, or 8) universally unique identifier (UUID). -->
検証対象のフィールドは、有効な RFC 9562 (バージョン 1、3、4、5、6、7、または 8) の汎用一意識別子 (UUID) である必要があります。

<!-- You may also validate that the given UUID matches a UUID specification by version: -->
指定された UUID がバージョンごとの UUID 仕様と一致することを検証することもできます。

```php
'uuid' => ['uuid:4']
```

<a name="conditionally-adding-rules"></a>
<!-- ## Conditionally Adding Rules -->
## Conditionally Adding Rules

<a name="skipping-validation-when-fields-have-certain-values"></a>
<!-- #### Skipping Validation When Fields Have Certain Values -->
#### Skipping Validation When Fields Have Certain Values

<!-- You may occasionally wish to not validate a given field if another field has a given value. You may accomplish this using the `exclude_if` validation rule. In this example, the `appointment_date` and `doctor_name` fields will not be validated if the `has_appointment` field has a value of `false`: -->
別のフィールドに特定の値がある場合、特定のフィールドを検証したくない場合があります。これは、`exclude_if` 検証ルールを使用して実行できます。この例では、`has_appointment` フィールドの値が `false` である場合、`appointment_date` フィールドと `doctor_name` フィールドは検証されません。

```php
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($data, [
    'has_appointment' => ['required', 'boolean'],
    'appointment_date' => ['exclude_if:has_appointment,false', 'required', 'date'],
    'doctor_name' => ['exclude_if:has_appointment,false', 'required', 'string'],
]);
```

<!-- Alternatively, you may use the `exclude_unless` rule to not validate a given field unless another field has a given value: -->
あるいは、`exclude_unless` ルールを使用して、別のフィールドに特定の値がない限り、特定のフィールドを検証しないこともできます。

```php
$validator = Validator::make($data, [
    'has_appointment' => ['required', 'boolean'],
    'appointment_date' => ['exclude_unless:has_appointment,true', 'required', 'date'],
    'doctor_name' => ['exclude_unless:has_appointment,true', 'required', 'string'],
]);
```

<a name="validating-when-present"></a>
<!-- #### Validating When Present -->
#### Validating When Present

<!-- In some situations, you may wish to run validation checks against a field **only** if that field is present in the data being validated. To quickly accomplish this, add the `sometimes` rule to your rule list: -->
状況によっては、フィールドが検証対象のデータに存在する場合にのみ**、そのフィールドに対して検証チェックを実行したい場合があります。これをすばやく実行するには、`sometimes` ルールをルール リストに追加します。

```php
$validator = Validator::make($data, [
    'email' => ['sometimes', 'required', 'email'],
]);
```

<!-- In the example above, the `email` field will only be validated if it is present in the `$data` array. -->
上記の例では、`email` フィールドは、`$data` 配列に存在する場合にのみ検証されます。

> [!NOTE]
> 常に存在する必要があるフィールドが空である可能性があることを検証しようとしている場合は、[this note on optional fields](#a-note-on-optional-fields) をチェックしてください。

<a name="complex-conditional-validation"></a>
<!-- #### Complex Conditional Validation -->
#### Complex Conditional Validation

<!-- Sometimes you may wish to add validation rules based on more complex conditional logic. For example, you may wish to require a given field only if another field has a greater value than 100. Or, you may need two fields to have a given value only when another field is present. Adding these validation rules doesn't have to be a pain. First, create a `Validator` instance with your _static rules_ that never change: -->
場合によっては、より複雑な条件ロジックに基づいた検証ルールを追加したい場合があります。たとえば、別のフィールドの値が 100 より大きい場合にのみ、特定のフィールドを必須にすることができます。または、別のフィールドが存在する場合にのみ、2 つのフィールドに特定の値を設定する必要がある場合があります。これらの検証ルールの追加は、それほど難しいことではありません。まず、決して変更されない_静的ルール_を使用して `Validator` インスタンスを作成します。

```php
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($request->all(), [
    'email' => ['required', 'email'],
    'games' => ['required', 'integer', 'min:0'],
]);
```

<!-- Let's assume our web application is for game collectors. If a game collector registers with our application and they own more than 100 games, we want them to explain why they own so many games. For example, perhaps they run a game resale shop, or maybe they just enjoy collecting games. To conditionally add this requirement, we can use the `sometimes` method on the `Validator` instance. -->
Web アプリケーションがゲーム コレクター向けであると仮定しましょう。ゲームコレクターが当社のアプリケーションに登録し、100 以上のゲームを所有している場合、なぜそんなに多くのゲームを所有しているのか説明してもらいたいと考えています。たとえば、ゲームの再販ショップを経営しているかもしれませんし、単にゲームを収集するのが趣味かもしれません。この要件を条件付きで追加するには、`Validator` インスタンスで `sometimes` メソッドを使用します。

```php
use Illuminate\Support\Fluent;

$validator->sometimes('reason', ['required', 'max:500'], function (Fluent $input) {
    return $input->games >= 100;
});
```

<!-- The first argument passed to the `sometimes` method is the name of the field we are conditionally validating. The second argument is a list of the rules we want to add. If the closure passed as the third argument returns `true`, the rules will be added. This method makes it a breeze to build complex conditional validations. You may even add conditional validations for several fields at once: -->
`sometimes` メソッドに渡される最初の引数は、条件付きで検証するフィールドの名前です。 2 番目の引数は、追加するルールのリストです。 3 番目の引数として渡されたクロージャが `true` を返す場合、ルールが追加されます。この方法を使用すると、複雑な条件付き検証を簡単に構築できます。複数のフィールドの条件付き検証を一度に追加することもできます。

```php
$validator->sometimes(['reason', 'cost'], 'required', function (Fluent $input) {
    return $input->games >= 100;
});
```

> [!NOTE]
> クロージャーに渡される `$input` パラメーターは `Illuminate\Support\Fluent` のインスタンスとなり、検証中の入力およびファイルにアクセスするために使用される場合があります。

<a name="complex-conditional-array-validation"></a>
<!-- #### Complex Conditional Array Validation -->
#### Complex Conditional Array Validation

<!-- Sometimes you may want to validate a field based on another field in the same nested array whose index you do not know. In these situations, you may allow your closure to receive a second argument which will be the current individual item in the array being validated: -->
同じ入れ子配列内のインデックスが不明な別のフィールドに基づいてフィールドを検証したい場合があります。このような状況では、クロージャが検証中の配列内の現在の個々の項目となる 2 番目の引数を受け取ることを許可できます。

```php
$input = [
    'channels' => [
        [
            'type' => 'email',
            'address' => 'abigail@example.com',
        ],
        [
            'type' => 'url',
            'address' => 'https://example.com',
        ],
    ],
];

$validator->sometimes('channels.*.address', 'email', function (Fluent $input, Fluent $item) {
    return $item->type === 'email';
});

$validator->sometimes('channels.*.address', 'url', function (Fluent $input, Fluent $item) {
    return $item->type !== 'email';
});
```

<!-- Like the `$input` parameter passed to the closure, the `$item` parameter is an instance of `Illuminate\Support\Fluent` when the attribute data is an array; otherwise, it is a string. -->
クロージャに渡される `$input` パラメータと同様、属性データが配列の場合、`$item` パラメータは `Illuminate\Support\Fluent` のインスタンスになります。それ以外の場合は文字列です。

<a name="validating-arrays"></a>
<!-- ## Validating Arrays -->
## Validating Arrays

<!-- As discussed in the [array validation rule documentation](#rule-array), the `array` rule accepts a list of allowed array keys. If any additional keys are present within the array, validation will fail: -->
[array validation rule documentation](#rule-array) で説明したように、`array` ルールは、許可された配列キーのリストを受け入れます。配列内に追加のキーが存在する場合、検証は失敗します。

```php
use Illuminate\Support\Facades\Validator;

$input = [
    'user' => [
        'name' => 'Taylor Otwell',
        'username' => 'taylorotwell',
        'admin' => true,
    ],
];

Validator::make($input, [
    'user' => ['array:name,username'],
]);
```

<!-- In general, you should always specify the array keys that are allowed to be present within your array. Otherwise, the validator's `validate` and `validated` methods will return all of the validated data, including the array and all of its keys, even if those keys were not validated by other nested array validation rules. -->
一般に、配列内に存在できる配列キーを常に指定する必要があります。それ以外の場合、バリデーターの `validate` メソッドと `validated` メソッドは、配列とそのすべてのキーを含む、検証されたすべてのデータを返します (それらのキーが他のネストされた配列検証ルールで検証されなかった場合でも)。

<a name="validating-nested-array-input"></a>
<!-- ### Validating Nested Array Input -->
### Validating Nested Array Input

<!-- Validating nested array-based form input fields doesn't have to be a pain. You may use "dot notation" to validate attributes within an array. For example, if the incoming HTTP request contains a `photos[profile]` field, you may validate it like so: -->
ネストされた配列ベースのフォーム入力フィールドの検証は、それほど面倒なことではありません。 「ドット表記」を使用して、配列内の属性を検証できます。たとえば、受信した HTTP リクエストに `photos[profile]` フィールドが含まれている場合、次のように検証できます。

```php
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($request->all(), [
    'photos.profile' => ['required', 'image'],
]);
```

<!-- You may also validate each element of an array. For example, to validate that each email in a given array input field is unique, you may do the following: -->
配列の各要素を検証することもできます。たとえば、特定の配列入力フィールド内の各電子メールが一意であることを検証するには、次の手順を実行します。

```php
$validator = Validator::make($request->all(), [
    'users.*.email' => ['email', 'unique:users'],
    'users.*.first_name' => ['required_with:users.*.last_name'],
]);
```

<!-- Likewise, you may use the `*` character when specifying [custom validation messages in your language files](#custom-messages-for-specific-attributes), making it a breeze to use a single validation message for array-based fields: -->
同様に、[custom validation messages in your language files](#custom-messages-for-specific-attributes) を指定するときに `*` 文字を使用すると、配列ベースのフィールドに単一の検証メッセージを簡単に使用できるようになります。

```php
'custom' => [
    'users.*.email' => [
        'unique' => 'Each user must have a unique email address',
    ]
],
```

<a name="accessing-nested-array-data"></a>
<!-- #### Accessing Nested Array Data -->
#### Accessing Nested Array Data

<!-- Sometimes you may need to access the value for a given nested array element when assigning validation rules to the attribute. You may accomplish this using the `Rule::forEach` method. The `forEach` method accepts a closure that will be invoked for each iteration of the array attribute under validation and will receive the attribute's value and explicit, fully-expanded attribute name. The closure should return an array of rules to assign to the array element: -->
属性に検証ルールを割り当てるときに、特定のネストされた配列要素の値にアクセスする必要がある場合があります。これは、`Rule::forEach` メソッドを使用して実行できます。 `forEach` メソッドは、検証中の配列属性の反復ごとに呼び出されるクロージャを受け入れ、属性の値と明示的な完全に展開された属性名を受け取ります。クロージャは、配列要素に割り当てるルールの配列を返す必要があります。

```php
use App\Rules\HasPermission;
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

$validator = Validator::make($request->all(), [
    'companies.*.id' => Rule::forEach(function (string|null $value, string $attribute) {
        return [
            Rule::exists(Company::class, 'id'),
            new HasPermission('manage-company', $value),
        ];
    }),
]);
```

<a name="error-message-indexes-and-positions"></a>
<!-- ### Error Message Indexes and Positions -->
### Error Message Indexes and Positions

<!-- When validating arrays, you may want to reference the index or position of a particular item that failed validation within the error message displayed by your application. To accomplish this, you may include the `:index` (starts from `0`), `:position` (starts from `1`), or `:ordinal-position` (starts from `1st`) placeholders within your [custom validation message](#manual-customizing-the-error-messages): -->
配列を検証するとき、アプリケーションによって表示されるエラー メッセージ内の検証に失敗した特定の項目のインデックスまたは位置を参照したい場合があります。これを実現するには、`:index` (`0` から始まる)、`:position` (`1` から始まる)、または `:ordinal-position` (`1st` から始まる) プレースホルダーを [custom validation message](#manual-customizing-the-error-messages) 内に含めることができます。

```php
use Illuminate\Support\Facades\Validator;

$input = [
    'photos' => [
        [
            'name' => 'BeachVacation.jpg',
            'description' => 'A photo of my beach vacation!',
        ],
        [
            'name' => 'GrandCanyon.jpg',
            'description' => '',
        ],
    ],
];

Validator::validate($input, [
    'photos.*.description' => ['required'],
], [
    'photos.*.description.required' => 'Please describe photo #:position.',
]);
```

<!-- Given the example above, validation will fail and the user will be presented with the following error of _"Please describe photo #2."_ -->
上記の例では、検証は失敗し、ユーザーには _「写真 #2 について説明してください。」_ というエラーが表示されます。

<!-- If necessary, you may reference more deeply nested indexes and positions via `second-index`, `second-position`, `third-index`, `third-position`, etc. -->
必要に応じて、`second-index`、`second-position`、`third-index`、`third-position` などを介して、より深くネストされたインデックスと位置を参照できます。

```php
'photos.*.attributes.*.string' => 'Invalid attribute for photo #:second-position.',
```

<a name="validating-files"></a>
<!-- ## Validating Files -->
## Validating Files

<!-- Laravel provides a variety of validation rules that may be used to validate uploaded files, such as `mimes`, `image`, `min`, and `max`. While you are free to specify these rules individually when validating files, Laravel also offers a fluent file validation rule builder that you may find convenient: -->
Laravel は、`mimes`、`image`、`min`、`max` など、アップロードされたファイルの検証に使用できるさまざまな検証ルールを提供します。ファイルを検証するときにこれらのルールを個別に自由に指定できますが、Laravel では、便利だと思われる滑らかなファイル検証ルール ビルダも提供しています。

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rules\File;

Validator::validate($input, [
    'attachment' => [
        'required',
        File::types(['mp3', 'wav'])
            ->min(1024)
            ->max(12 * 1024),
    ],
]);
```

<a name="validating-files-file-types"></a>
<!-- #### Validating File Types -->
#### Validating File Types

<!-- Even though you only need to specify the extensions when invoking the `types` method, this method actually validates the MIME type of the file by reading the file's contents and guessing its MIME type. A full listing of MIME types and their corresponding extensions may be found at the following location: -->
`types` メソッドを呼び出すときに拡張子を指定するだけで済みますが、このメソッドは実際にファイルの内容を読み取り、その MIME タイプを推測することでファイルの MIME タイプを検証します。 MIME タイプとそれに対応する拡張子の完全なリストは、次の場所にあります。

<!-- [https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types](https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types) -->
[https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types](https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types)

<a name="validating-files-file-sizes"></a>
<!-- #### Validating File Sizes -->
#### Validating File Sizes

<!-- For convenience, minimum and maximum file sizes may be specified as a string with a suffix indicating the file size units. The `kb`, `mb`, `gb`, and `tb` suffixes are supported: -->
便宜上、最小および最大ファイル サイズは、ファイル サイズ単位を示す接尾辞を付けた文字列として指定できます。 `kb`、`mb`、`gb`、および `tb` サフィックスがサポートされています。

```php
File::types(['mp3', 'wav'])
    ->min('1kb')
    ->max('10mb');
```

<a name="validating-files-image-files"></a>
<!-- #### Validating Image Files -->
#### Validating Image Files

<!-- If your application accepts images uploaded by your users, you may use the `File` rule's `image` constructor method to ensure that the file under validation is an image (jpg, jpeg, png, bmp, gif, or webp). -->
アプリケーションがユーザーによってアップロードされた画像を受け入れる場合、`File` ルールの `image` コンストラクター メソッドを使用して、検証中のファイルが画像 (jpg、jpeg、png、bmp、gif、または webp) であることを確認できます。

<!-- In addition, the `dimensions` rule may be used to limit the dimensions of the image: -->
さらに、`dimensions` ルールを使用して画像のサイズを制限することもできます。

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;
use Illuminate\Validation\Rules\File;

Validator::validate($input, [
    'photo' => [
        'required',
        File::image()
            ->min(1024)
            ->max(12 * 1024)
            ->dimensions(Rule::dimensions()->maxWidth(1000)->maxHeight(500)),
    ],
]);
```

> [!NOTE]
> 画像の寸法の検証に関する詳細については、[dimension rule documentation](#rule-dimensions) を参照してください。

> [!WARNING]
> XSS 脆弱性の可能性があるため、デフォルトでは、`image` ルールは SVG ファイルを許可しません。 SVG ファイルを許可する必要がある場合は、`allowSvg: true` を `image` ルールに渡すことができます: `File::image(allowSvg: true)`。

<a name="validating-files-image-dimensions"></a>
<!-- #### Validating Image Dimensions -->
#### Validating Image Dimensions

<!-- You may also validate the dimensions of an image. For example, to validate that an uploaded image is at least 1000 pixels wide and 500 pixels tall, you may use the `dimensions` rule: -->
画像の寸法を検証することもできます。たとえば、アップロードされた画像が少なくとも幅 1000 ピクセル、高さ 500 ピクセルであることを検証するには、`dimensions` ルールを使用できます。

```php
use Illuminate\Validation\Rule;
use Illuminate\Validation\Rules\File;

File::image()->dimensions(
    Rule::dimensions()
        ->maxWidth(1000)
        ->maxHeight(500)
)
```

> [!NOTE]
> 画像の寸法の検証に関する詳細については、[dimension rule documentation](#rule-dimensions) を参照してください。

<a name="validating-passwords"></a>
<!-- ## Validating Passwords -->
## Validating Passwords

<!-- To ensure that passwords have an adequate level of complexity, you may use Laravel's `Password` rule object: -->
パスワードに適切なレベルの複雑さを持たせるには、Laravel の `Password` ルール オブジェクトを使用できます。

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rules\Password;

$validator = Validator::make($request->all(), [
    'password' => ['required', 'confirmed', Password::min(8)],
]);
```

<!-- The `Password` rule object allows you to easily customize the password complexity requirements for your application, such as specifying that passwords require at least one letter, number, symbol, or characters with mixed casing: -->
`Password` ルール オブジェクトを使用すると、パスワードに少なくとも 1 つの文字、数字、記号、または大文字と小文字が混在する文字が必要であることを指定するなど、アプリケーションのパスワードの複雑さの要件を簡単にカスタマイズできます。

```php
// Require at least 8 characters...
Password::min(8)

// Require at most 256 characters...
Password::min(16)->max(256)

// Require at least one letter...
Password::min(8)->letters()

// Require at least one uppercase and one lowercase letter...
Password::min(8)->mixedCase()

// Require at least one number...
Password::min(8)->numbers()

// Require at least one symbol...
Password::min(8)->symbols()
```

<!-- In addition, you may ensure that a password has not been compromised in a public password data breach leak using the `uncompromised` method: -->
さらに、`uncompromised` メソッドを使用して、パブリック パスワード データ漏洩でパスワードが侵害されていないことを確認できます。

```php
Password::min(8)->uncompromised()
```

<!-- Internally, the `Password` rule object uses the [k-Anonymity](https://en.wikipedia.org/wiki/K-anonymity) model to determine if a password has been leaked via the [haveibeenpwned.com](https://haveibeenpwned.com) service without sacrificing the user's privacy or security. -->
内部的には、`Password` ルール オブジェクトは [k-Anonymity](https://en.wikipedia.org/wiki/K-anonymity) モデルを使用して、ユーザーのプライバシーやセキュリティを犠牲にすることなく、パスワードが [haveibeenpwned.com](https://haveibeenpwned.com) サービス経由で漏洩したかどうかを判断します。

<!-- By default, if a password appears at least once in a data leak, it will be considered compromised. You can customize this threshold using the first argument of the `uncompromised` method: -->
デフォルトでは、パスワードがデータ漏洩の際に少なくとも 1 回出現すると、そのパスワードは侵害されたとみなされます。このしきい値は、`uncompromised` メソッドの最初の引数を使用してカスタマイズできます。

```php
// Ensure the password appears less than 3 times in the same data leak...
Password::min(8)->uncompromised(3);
```

<!-- Of course, you may chain all the methods in the examples above: -->
もちろん、上記の例のすべてのメソッドを連鎖させることもできます。

```php
Password::min(8)
    ->max(256)
    ->letters()
    ->mixedCase()
    ->numbers()
    ->symbols()
    ->uncompromised()
```

<!-- You may convert a `Password` rule object to a string suitable for the HTML `passwordrules` attribute using the `toPasswordRulesString` method: -->
`toPasswordRulesString` メソッドを使用して、`Password` ルール オブジェクトを HTML `passwordrules` 属性に適した文字列に変換できます。

```blade
<input
    type="password"
    name="password"
    autocomplete="new-password"
    passwordrules="{{ Password::defaults()->toPasswordRulesString() }}"
/>
```

<a name="defining-default-password-rules"></a>
<!-- #### Defining Default Password Rules -->
#### Defining Default Password Rules

<!-- You may find it convenient to specify the default validation rules for passwords in a single location of your application. You can easily accomplish this using the `Password::defaults` method, which accepts a closure. The closure given to the `defaults` method should return the default configuration of the Password rule. Typically, the `defaults` rule should be called within the `boot` method of one of your application's service providers: -->
アプリケーションの単一の場所でパスワードのデフォルトの検証ルールを指定すると便利な場合があります。これは、クロージャを受け入れる `Password::defaults` メソッドを使用して簡単に実現できます。 `defaults` メソッドに指定されたクロージャは、パスワード ルールのデフォルト設定を返す必要があります。通常、`defaults` ルールは、アプリケーションのサービスプロバイダの 1 つの `boot` メソッド内で呼び出す必要があります。

```php
use Illuminate\Validation\Rules\Password;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Password::defaults(function () {
        $rule = Password::min(8);

        return $this->app->isProduction()
            ? $rule->mixedCase()->uncompromised()
            : $rule;
    });
}
```

<!-- Then, when you would like to apply the default rules to a particular password undergoing validation, you may invoke the `defaults` method with no arguments: -->
次に、検証中の特定のパスワードにデフォルトのルールを適用したい場合は、引数なしで `defaults` メソッドを呼び出すことができます。

```php
'password' => ['required', Password::defaults()],
```

<!-- Occasionally, you may want to attach additional validation rules to your default password validation rules. You may use the `rules` method to accomplish this: -->
場合によっては、デフォルトのパスワード検証ルールに追加の検証ルールを追加することが必要になる場合があります。これを実現するには、`rules` メソッドを使用できます。

```php
use App\Rules\ZxcvbnRule;

Password::defaults(function () {
    $rule = Password::min(8)->rules([new ZxcvbnRule]);

    // ...
});
```

<a name="custom-validation-rules"></a>
<!-- ## Custom Validation Rules -->
## Custom Validation Rules

<a name="using-rule-objects"></a>
<!-- ### Using Rule Objects -->
### Using Rule Objects

<!-- Laravel provides a variety of helpful validation rules; however, you may wish to specify some of your own. One method of registering custom validation rules is using rule objects. To generate a new rule object, you may use the `make:rule` Artisan command. Let's use this command to generate a rule that verifies a string is uppercase. Laravel will place the new rule in the `app/Rules` directory. If this directory does not exist, Laravel will create it when you execute the Artisan command to create your rule: -->
Laravel は、さまざまな便利な検証ルールを提供します。ただし、独自のものを指定したい場合もあります。カスタム検証ルールを登録する 1 つの方法は、ルール オブジェクトを使用することです。新しいルール オブジェクトを生成するには、`make:rule` Artisan コマンドを使用できます。このコマンドを使用して、文字列が大文字であることを検証するルールを生成してみましょう。 Laravel は新しいルールを `app/Rules` ディレクトリに配置します。このディレクトリが存在しない場合、Artisan コマンドを実行してルールを作成すると、Laravel によってディレクトリが作成されます。

```shell
php artisan make:rule Uppercase
```

<!-- Once the rule has been created, we are ready to define its behavior. A rule object contains a single method: `validate`. This method receives the attribute name, its value, and a callback that should be invoked on failure with the validation error message: -->
ルールを作成したら、その動作を定義する準備が整います。ルール オブジェクトには、`validate` という 1 つのメソッドが含まれています。このメソッドは、属性名、その値、および検証エラー メッセージが表示されて失敗した場合に呼び出されるコールバックを受け取ります。

```php
<?php

namespace App\Rules;

use Closure;
use Illuminate\Contracts\Validation\ValidationRule;

class Uppercase implements ValidationRule
{
    /**
     * Run the validation rule.
     */
    public function validate(string $attribute, mixed $value, Closure $fail): void
    {
        if (strtoupper($value) !== $value) {
            $fail('The :attribute must be uppercase.');
        }
    }
}
```

<!-- Once the rule has been defined, you may attach it to a validator by passing an instance of the rule object with your other validation rules: -->
ルールを定義したら、他の検証ルールとともにルール オブジェクトのインスタンスを渡すことで、ルールをバリデーターに添付できます。

```php
use App\Rules\Uppercase;

$request->validate([
    'name' => ['required', 'string', new Uppercase],
]);
```

<!-- #### Translating Validation Messages -->
#### Translating Validation Messages

<!-- Instead of providing a literal error message to the `$fail` closure, you may also provide a [translation string key](/docs/13.x/localization) and instruct Laravel to translate the error message: -->
リテラルのエラーメッセージを `$fail` クロージャーに提供する代わりに、[translation string key](/docs/13.x/localization) を提供して、エラーメッセージを翻訳するように Laravel に指示することもできます。

```php
if (strtoupper($value) !== $value) {
    $fail('validation.uppercase')->translate();
}
```

<!-- If necessary, you may provide placeholder replacements and the preferred language as the first and second arguments to the `translate` method: -->
必要に応じて、プレースホルダー置換と優先言語を `translate` メソッドの最初と 2 番目の引数として指定できます。

```php
$fail('validation.location')->translate([
    'value' => $this->value,
], 'fr');
```

<!-- #### Accessing Additional Data -->
#### Accessing Additional Data

<!-- If your custom validation rule class needs to access all of the other data undergoing validation, your rule class may implement the `Illuminate\Contracts\Validation\DataAwareRule` interface. This interface requires your class to define a `setData` method. This method will automatically be invoked by Laravel (before validation proceeds) with all of the data under validation: -->
カスタム検証ルール クラスが検証中の他のすべてのデータにアクセスする必要がある場合、ルール クラスは `Illuminate\Contracts\Validation\DataAwareRule` インターフェイスを実装できます。このインターフェイスでは、クラスで `setData` メソッドを定義する必要があります。このメソッドは、検証中のすべてのデータを使用して、Laravel によって (検証が続行する前に) 自動的に呼び出されます。

```php
<?php

namespace App\Rules;

use Illuminate\Contracts\Validation\DataAwareRule;
use Illuminate\Contracts\Validation\ValidationRule;

class Uppercase implements DataAwareRule, ValidationRule
{
    /**
     * All of the data under validation.
     *
     * @var array<string, mixed>
     */
    protected $data = [];

    // ...

    /**
     * Set the data under validation.
     *
     * @param  array<string, mixed>  $data
     */
    public function setData(array $data): static
    {
        $this->data = $data;

        return $this;
    }
}
```

<!-- Or, if your validation rule requires access to the validator instance performing the validation, you may implement the `ValidatorAwareRule` interface: -->
または、検証ルールで検証を実行するバリデーター インスタンスへのアクセスが必要な場合は、`ValidatorAwareRule` インターフェイスを実装できます。

```php
<?php

namespace App\Rules;

use Illuminate\Contracts\Validation\ValidationRule;
use Illuminate\Contracts\Validation\ValidatorAwareRule;
use Illuminate\Validation\Validator;

class Uppercase implements ValidationRule, ValidatorAwareRule
{
    /**
     * The validator instance.
     *
     * @var \Illuminate\Validation\Validator
     */
    protected $validator;

    // ...

    /**
     * Set the current validator.
     */
    public function setValidator(Validator $validator): static
    {
        $this->validator = $validator;

        return $this;
    }
}
```

<a name="using-closures"></a>
<!-- ### Using Closures -->
### Using Closures

<!-- If you only need the functionality of a custom rule once throughout your application, you may use a closure instead of a rule object. The closure receives the attribute's name, the attribute's value, and a `$fail` callback that should be called if validation fails: -->
アプリケーション全体でカスタム ルールの機能が 1 回だけ必要な場合は、ルール オブジェクトの代わりにクロージャを使用できます。クロージャは、属性の名前、属性の値、および検証が失敗した場合に呼び出される `$fail` コールバックを受け取ります。

```php
use Illuminate\Support\Facades\Validator;
use Closure;

$validator = Validator::make($request->all(), [
    'title' => [
        'required',
        'max:255',
        function (string $attribute, mixed $value, Closure $fail) {
            if ($value === 'foo') {
                $fail("The {$attribute} is invalid.");
            }
        },
    ],
]);
```

<a name="implicit-rules"></a>
<!-- ### Implicit Rules -->
### Implicit Rules

<!-- By default, when an attribute being validated is not present or contains an empty string, normal validation rules, including custom rules, are not run. For example, the [unique](#rule-unique) rule will not be run against an empty string: -->
デフォルトでは、検証対象の属性が存在しないか、空の文字列が含まれている場合、カスタム ルールを含む通常の検証ルールは実行されません。たとえば、[unique](#rule-unique) ルールは空の文字列に対しては実行されません。

```php
use Illuminate\Support\Facades\Validator;

$rules = ['name' => ['unique:users,name']];

$input = ['name' => ''];

Validator::make($input, $rules)->passes(); // true
```

<!-- For a custom rule to run even when an attribute is empty, the rule must imply that the attribute is required. To quickly generate a new implicit rule object, you may use the `make:rule` Artisan command with the `--implicit` option: -->
属性が空の場合でもカスタム ルールを実行するには、その属性が必須であることをルールで暗黙的に示す必要があります。新しい暗黙的ルール オブジェクトをすばやく生成するには、`make:rule` Artisan コマンドを `--implicit` オプションとともに使用します。

```shell
php artisan make:rule Uppercase --implicit
```

> [!WARNING]
> 「暗黙の」ルールは、属性が必須であることを_暗黙的に示すだけです。欠落している属性または空の属性を実際に無効にするかどうかは、ユーザー次第です。
