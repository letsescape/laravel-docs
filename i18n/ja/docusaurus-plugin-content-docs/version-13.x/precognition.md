# 予知 (Precognition)

- [Introduction](#introduction)
- [ライブ検証](#live-validation)
    - [Vueの使用](#using-vue)
    - [反応の使用](#using-react)
    - [Alpine と Blade の使用](#using-alpine)
    - [Axiosの構成](#configuring-axios)
- [配列の検証](#validating-arrays)
- [検証ルールのカスタマイズ](#customizing-validation-rules)
- [ファイルのアップロードの処理](#handling-file-uploads)
- [副作用の管理](#managing-side-effects)
- [Testing](#testing)

<a name="introduction"></a>
## 導入 (Introduction)

Laravel Precognition を使用すると、将来の HTTP リクエストの結果を予測できます。 Precognition の主な使用例の 1 つは、アプリケーションのバックエンド検証ルールを複製することなく、フロントエンド JavaScript アプリケーションに「ライブ」検証を提供できることです。

Laravel が「事前認識リクエスト」を受信すると、ルートのすべてのミドルウェアが実行され、[フォームリクエスト](/docs/{{version}}/validation#form-request-validation) の検証を含むルートのコントローラの依存関係が解決されますが、実際にはルートのコントローラ メソッドは実行されません。

> [!NOTE]
> Inertia 2.3 では、Precognition サポートが組み込まれています。詳細については、[Inertiaフォームのドキュメント](https://inertiajs.com/forms) を参照してください。以前の Inertia バージョンには Precognition 0.x が必要です。

<a name="live-validation"></a>
## ライブ検証 (Live Validation)

<a name="using-vue"></a>
### Vueの使用

Laravel Precognition を使用すると、フロントエンド Vue アプリケーションで検証ルールを複製することなく、ライブ検証エクスペリエンスをユーザーに提供できます。その仕組みを説明するために、アプリケーション内で新しいユーザーを作成するためのフォームを構築してみましょう。

まず、ルートの事前認識を有効にするには、`HandlePrecognitiveRequests` ミドルウェアをルート定義に追加する必要があります。ルートの検証ルールを格納する [フォームリクエスト](/docs/{{version}}/validation#form-request-validation) も作成する必要があります。

```php
use App\Http\Requests\StoreUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (StoreUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```

次に、NPM 経由で Vue 用の Laravel Precognition フロントエンド ヘルパをインストールする必要があります。

```shell
npm install laravel-precognition-vue
```

Laravel Precognition パッケージがインストールされていると、Precognition の `useForm` 関数を使用してフォーム オブジェクトを作成し、HTTP メソッド (`post`)、ターゲット URL (`/users`)、および初期フォーム データを提供できるようになります。

次に、ライブ検証を有効にするには、入力の名前を指定して、各入力の `change` イベントでフォームの `validate` メソッドを呼び出します。

```vue
<script setup>
import { useForm } from 'laravel-precognition-vue';

const form = useForm('post', '/users', {
    name: '',
    email: '',
});

const submit = () => form.submit();
</script>

<template>
    <form @submit.prevent="submit">
        <label for="name">Name</label>
        <input
            id="name"
            v-model="form.name"
            @change="form.validate('name')"
        />
        <div v-if="form.invalid('name')">
            {{ form.errors.name }}
        </div>

        <label for="email">Email</label>
        <input
            id="email"
            type="email"
            v-model="form.email"
            @change="form.validate('email')"
        />
        <div v-if="form.invalid('email')">
            {{ form.errors.email }}
        </div>

        <button :disabled="form.processing">
            Create User
        </button>
    </form>
</template>
```

ユーザーがフォームに入力すると、Precognition はルートのフォーム リクエスト内の検証ルールを活用したライブ検証出力を提供します。フォームの入力が変更されると、デバウンスされた「プリコグニティブ」検証リクエストが Laravel アプリケーションに送信されます。フォームの `setValidationTimeout` 関数を呼び出すことで、デバウンス タイムアウトを構成できます。

```js
form.setValidationTimeout(3000);
```

検証リクエストが進行中の場合、フォームの `validating` プロパティは `true` になります。

```html
<div v-if="form.validating">
    Validating...
</div>
```

検証リクエストまたはフォームの送信中に返された検証エラーは、フォームの `errors` オブジェクトに自動的に設定されます。

```html
<div v-if="form.invalid('email')">
    {{ form.errors.email }}
</div>
```

フォームの `hasErrors` プロパティを使用して、フォームにエラーがあるかどうかを確認できます。

```html
<div v-if="form.hasErrors">
    <!-- ... -->
</div>
```

入力の名前をフォームの `valid` 関数と `invalid` 関数にそれぞれ渡すことで、入力が検証に合格したか失敗したかを判断することもできます。

```html
<span v-if="form.valid('email')">
    ✅
</span>

<span v-else-if="form.invalid('email')">
    ❌
</span>
```

> [!WARNING]
> フォーム入力は、変更されて検証応答が受信された場合にのみ、有効または無効として表示されます。

Precognition を使用してフォームの入力のサブセットを検証している場合、エラーを手動でクリアすると便利な場合があります。これを実現するには、フォームの `forgetError` 関数を使用できます。

```html
<input
    id="avatar"
    type="file"
    @change="(e) => {
        form.avatar = e.target.files[0]

        form.forgetError('avatar')
    }"
>
```

これまで見てきたように、入力の `change` イベントにフックして、ユーザーが操作する個々の入力を検証できます。ただし、ユーザーがまだ操作していない入力を検証する必要がある場合があります。これは、次のステップに進む前に、ユーザーが操作したかどうかに関係なく、表示されているすべての入力を検証する「ウィザード」を構築する場合に一般的です。

Precognition を使用してこれを行うには、`validate` メソッドを呼び出して、検証するフィールド名を `only` 構成キーに渡す必要があります。検証結果は、`onSuccess` または `onValidationError` コールバックで処理できます。

```html
<button
    type="button"
    @click="form.validate({
        only: ['name', 'email', 'phone'],
        onSuccess: (response) => nextStep(),
        onValidationError: (response) => /* ... */,
    })"
>Next Step</button>
```

もちろん、フォーム送信に対する応答に応じてコードを実行することもできます。フォームの `submit` 関数は、Axios リクエストの Promise を返します。これにより、応答ペイロードにアクセスしたり、送信成功時にフォーム入力をリセットしたり、失敗したリクエストを処理したりするための便利な方法が提供されます。

```js
const submit = () => form.submit()
    .then(response => {
        form.reset();

        alert('User created.');
    })
    .catch(error => {
        alert('An error occurred.');
    });
```

フォームの `processing` プロパティを検査することで、フォーム送信リクエストが処理中かどうかを判断できます。

```html
<button :disabled="form.processing">
    Submit
</button>
```

<a name="using-react"></a>
### 反応の使用

Laravel Precognition を使用すると、フロントエンド React アプリケーションで検証ルールを複製することなく、ライブ検証エクスペリエンスをユーザーに提供できます。その仕組みを説明するために、アプリケーション内で新しいユーザーを作成するためのフォームを構築してみましょう。

まず、ルートの事前認識を有効にするには、`HandlePrecognitiveRequests` ミドルウェアをルート定義に追加する必要があります。ルートの検証ルールを格納する [フォームリクエスト](/docs/{{version}}/validation#form-request-validation) も作成する必要があります。

```php
use App\Http\Requests\StoreUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (StoreUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```

次に、NPM 経由で React 用の Laravel Precognition フロントエンド ヘルパをインストールする必要があります。

```shell
npm install laravel-precognition-react
```

Laravel Precognition パッケージがインストールされていると、Precognition の `useForm` 関数を使用してフォーム オブジェクトを作成し、HTTP メソッド (`post`)、ターゲット URL (`/users`)、および初期フォーム データを提供できるようになります。

ライブ検証を有効にするには、各入力の `change` および `blur` イベントをリッスンする必要があります。 `change` イベント ハンドラーでは、`setData` 関数を使用してフォームのデータを設定し、入力の名前と新しい値を渡す必要があります。次に、`blur` イベント ハンドラーで、入力の名前を指定してフォームの `validate` メソッドを呼び出します。

```jsx
import { useForm } from 'laravel-precognition-react';

export default function Form() {
    const form = useForm('post', '/users', {
        name: '',
        email: '',
    });

    const submit = (e) => {
        e.preventDefault();

        form.submit();
    };

    return (
        <form onSubmit={submit}>
            <label htmlFor="name">Name</label>
            <input
                id="name"
                value={form.data.name}
                onChange={(e) => form.setData('name', e.target.value)}
                onBlur={() => form.validate('name')}
            />
            {form.invalid('name') && <div>{form.errors.name}</div>}

            <label htmlFor="email">Email</label>
            <input
                id="email"
                value={form.data.email}
                onChange={(e) => form.setData('email', e.target.value)}
                onBlur={() => form.validate('email')}
            />
            {form.invalid('email') && <div>{form.errors.email}</div>}

            <button disabled={form.processing}>
                Create User
            </button>
        </form>
    );
};
```

ユーザーがフォームに入力すると、Precognition はルートのフォーム リクエスト内の検証ルールを活用したライブ検証出力を提供します。フォームの入力が変更されると、デバウンスされた「プリコグニティブ」検証リクエストが Laravel アプリケーションに送信されます。フォームの `setValidationTimeout` 関数を呼び出すことで、デバウンス タイムアウトを構成できます。

```js
form.setValidationTimeout(3000);
```

検証リクエストが進行中の場合、フォームの `validating` プロパティは `true` になります。

```jsx
{form.validating && <div>Validating...</div>}
```

検証リクエストまたはフォームの送信中に返された検証エラーは、フォームの `errors` オブジェクトに自動的に設定されます。

```jsx
{form.invalid('email') && <div>{form.errors.email}</div>}
```

フォームの `hasErrors` プロパティを使用して、フォームにエラーがあるかどうかを確認できます。

```jsx
{form.hasErrors && <div><!-- ... --></div>}
```

入力の名前をフォームの `valid` 関数と `invalid` 関数にそれぞれ渡すことで、入力が検証に合格したか失敗したかを判断することもできます。

```jsx
{form.valid('email') && <span>✅</span>}

{form.invalid('email') && <span>❌</span>}
```

> [!WARNING]
> フォーム入力は、変更されて検証応答が受信された場合にのみ、有効または無効として表示されます。

Precognition を使用してフォームの入力のサブセットを検証している場合、エラーを手動でクリアすると便利な場合があります。これを実現するには、フォームの `forgetError` 関数を使用できます。

```jsx
<input
    id="avatar"
    type="file"
    onChange={(e) => {
        form.setData('avatar', e.target.files[0]);

        form.forgetError('avatar');
    }}
>
```

これまで見てきたように、入力の `blur` イベントにフックして、ユーザーが操作する個々の入力を検証できます。ただし、ユーザーがまだ操作していない入力を検証する必要がある場合があります。これは、次のステップに進む前に、ユーザーが操作したかどうかに関係なく、表示されているすべての入力を検証する「ウィザード」を構築する場合に一般的です。

Precognition を使用してこれを行うには、`validate` メソッドを呼び出して、検証するフィールド名を `only` 構成キーに渡す必要があります。検証結果は、`onSuccess` または `onValidationError` コールバックで処理できます。

```jsx
<button
    type="button"
    onClick={() => form.validate({
        only: ['name', 'email', 'phone'],
        onSuccess: (response) => nextStep(),
        onValidationError: (response) => /* ... */,
    })}
>Next Step</button>
```

もちろん、フォーム送信に対する応答に応じてコードを実行することもできます。フォームの `submit` 関数は、Axios リクエストの Promise を返します。これにより、応答ペイロードにアクセスしたり、フォーム送信が成功したときにフォームの入力をリセットしたり、失敗したリクエストを処理したりするための便利な方法が提供されます。

```js
const submit = (e) => {
    e.preventDefault();

    form.submit()
        .then(response => {
            form.reset();

            alert('User created.');
        })
        .catch(error => {
            alert('An error occurred.');
        });
};
```

フォームの `processing` プロパティを検査することで、フォーム送信リクエストが処理中かどうかを判断できます。

```html
<button disabled={form.processing}>
    Submit
</button>
```

<a name="using-alpine"></a>
### Alpine と Blade の使用

Laravel Precognition を使用すると、フロントエンド Alpine アプリケーションで検証ルールを複製することなく、ライブ検証エクスペリエンスをユーザーに提供できます。その仕組みを説明するために、アプリケーション内で新しいユーザーを作成するためのフォームを構築してみましょう。

まず、ルートの事前認識を有効にするには、`HandlePrecognitiveRequests` ミドルウェアをルート定義に追加する必要があります。ルートの検証ルールを格納する [フォームリクエスト](/docs/{{version}}/validation#form-request-validation) も作成する必要があります。

```php
use App\Http\Requests\CreateUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (CreateUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```

次に、NPM 経由で Alpine 用の Laravel Precognition フロントエンド ヘルパをインストールする必要があります。

```shell
npm install laravel-precognition-alpine
```

次に、`resources/js/app.js` ファイルで Precognition プラグインを Alpine に登録します。

```js
import Alpine from 'alpinejs';
import Precognition from 'laravel-precognition-alpine';

window.Alpine = Alpine;

Alpine.plugin(Precognition);
Alpine.start();
```

Laravel Precognition パッケージをインストールして登録すると、Precognition の `$form` "マジック" を使用してフォーム オブジェクトを作成し、HTTP メソッド (`post`)、ターゲット URL (`/users`)、および初期フォーム データを提供できるようになります。

ライブ検証を有効にするには、フォームのデータを関連する入力にバインドし、各入力の `change` イベントをリッスンする必要があります。 `change` イベント ハンドラーでは、入力の名前を指定してフォームの `validate` メソッドを呼び出す必要があります。

```html
<form x-data="{
    form: $form('post', '/register', {
        name: '',
        email: '',
    }),
}">
    @csrf
    <label for="name">Name</label>
    <input
        id="name"
        name="name"
        x-model="form.name"
        @change="form.validate('name')"
    />
    <template x-if="form.invalid('name')">
        <div x-text="form.errors.name"></div>
    </template>

    <label for="email">Email</label>
    <input
        id="email"
        name="email"
        x-model="form.email"
        @change="form.validate('email')"
    />
    <template x-if="form.invalid('email')">
        <div x-text="form.errors.email"></div>
    </template>

    <button :disabled="form.processing">
        Create User
    </button>
</form>
```

ユーザーがフォームに入力すると、Precognition はルートのフォーム リクエスト内の検証ルールを活用したライブ検証出力を提供します。フォームの入力が変更されると、デバウンスされた「プリコグニティブ」検証リクエストが Laravel アプリケーションに送信されます。フォームの `setValidationTimeout` 関数を呼び出すことで、デバウンス タイムアウトを構成できます。

```js
form.setValidationTimeout(3000);
```

検証リクエストが進行中の場合、フォームの `validating` プロパティは `true` になります。

```html
<template x-if="form.validating">
    <div>Validating...</div>
</template>
```

検証リクエストまたはフォームの送信中に返された検証エラーは、フォームの `errors` オブジェクトに自動的に設定されます。

```html
<template x-if="form.invalid('email')">
    <div x-text="form.errors.email"></div>
</template>
```

フォームの `hasErrors` プロパティを使用して、フォームにエラーがあるかどうかを確認できます。

```html
<template x-if="form.hasErrors">
    <div><!-- ... --></div>
</template>
```

入力の名前をフォームの `valid` 関数と `invalid` 関数にそれぞれ渡すことで、入力が検証に合格したか失敗したかを判断することもできます。

```html
<template x-if="form.valid('email')">
    <span>✅</span>
</template>

<template x-if="form.invalid('email')">
    <span>❌</span>
</template>
```

> [!WARNING]
> フォーム入力は、変更されて検証応答が受信された場合にのみ、有効または無効として表示されます。

これまで見てきたように、入力の `change` イベントにフックして、ユーザーが操作する個々の入力を検証できます。ただし、ユーザーがまだ操作していない入力を検証する必要がある場合があります。これは、次のステップに進む前に、ユーザーが操作したかどうかに関係なく、表示されているすべての入力を検証する「ウィザード」を構築する場合に一般的です。

Precognition を使用してこれを行うには、`validate` メソッドを呼び出して、検証するフィールド名を `only` 構成キーに渡す必要があります。検証結果は、`onSuccess` または `onValidationError` コールバックで処理できます。

```html
<button
    type="button"
    @click="form.validate({
        only: ['name', 'email', 'phone'],
        onSuccess: (response) => nextStep(),
        onValidationError: (response) => /* ... */,
    })"
>Next Step</button>
```

フォームの `processing` プロパティを検査することで、フォーム送信リクエストが処理中かどうかを判断できます。

```html
<button :disabled="form.processing">
    Submit
</button>
```

<a name="repopulating-old-form-data"></a>
#### 古いフォームデータを再入力する

上で説明したユーザー作成の例では、Precognition を使用してライブ検証を実行しています。ただし、フォームを送信するために従来のサーバー側のフォーム送信を実行しています。したがって、サーバー側のフォーム送信から返された「古い」入力エラーと検証エラーをフォームに入力する必要があります。

```html
<form x-data="{
    form: $form('post', '/register', {
        name: '{{ old('name') }}',
        email: '{{ old('email') }}',
    }).setErrors({{ Js::from($errors->messages()) }}),
}">
```

あるいは、XHR 経由でフォームを送信したい場合は、Axios リクエスト Promise を返すフォームの `submit` 関数を使用することもできます。

```html
<form
    x-data="{
        form: $form('post', '/register', {
            name: '',
            email: '',
        }),
        submit() {
            this.form.submit()
                .then(response => {
                    this.form.reset();

                    alert('User created.')
                })
                .catch(error => {
                    alert('An error occurred.');
                });
        },
    }"
    @submit.prevent="submit"
>
```

<a name="configuring-axios"></a>
### Axiosの構成

Precognition 検証ライブラリは、[Axios](https://github.com/axios/axios) HTTP クライアントを使用して、アプリケーションのバックエンドにリクエストを送信します。便宜上、アプリケーションで必要に応じて Axios インスタンスをカスタマイズできます。たとえば、`laravel-precognition-vue` ライブラリを使用する場合、アプリケーションの `resources/js/app.js` ファイル内の各送信リクエストに追加のリクエスト ヘッダーを追加できます。

```js
import { client } from 'laravel-precognition-vue';

client.axios().defaults.headers.common['Authorization'] = authToken;
```

または、アプリケーション用に構成された Axios インスタンスがすでにある場合は、代わりにそのインスタンスを使用するように Precognition に指示することもできます。

```js
import Axios from 'axios';
import { client } from 'laravel-precognition-vue';

window.axios = Axios.create()
window.axios.defaults.headers.common['Authorization'] = authToken;

client.use(window.axios)
```

<a name="validating-arrays"></a>
## 配列の検証 (Validating Arrays)

ワイルドカードを使用して、配列またはネストされたオブジェクト内のフィールドを検証できます。各 `*` は単一のパス セグメントと一致します。

```js
// Validate email for all users in an array...
form.validate('users.*.email');

// Validate all fields in a profile object...
form.validate('profile.*');

// Validate all fields for all users...
form.validate('users.*.*');
```

<a name="customizing-validation-rules"></a>
## 検証ルールのカスタマイズ (Customizing Validation Rules)

リクエストの `isPrecognitive` メソッドを使用して、予測リクエスト中に実行される検証ルールをカスタマイズできます。

たとえば、ユーザー作成フォームでは、最終的なフォーム送信時にのみパスワードが「侵害されていない」ことを検証したい場合があります。予知的検証リクエストの場合、パスワードが必須であり、最低 8 文字であることを単純に検証します。 `isPrecognitive` メソッドを使用すると、フォーム リクエストで定義されたルールをカスタマイズできます。

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rules\Password;

class StoreUserRequest extends FormRequest
{
    /**
     * Get the validation rules that apply to the request.
     *
     * @return array
     */
    protected function rules()
    {
        return [
            'password' => [
                'required',
                $this->isPrecognitive()
                    ? Password::min(8)
                    : Password::min(8)->uncompromised(),
            ],
            // ...
        ];
    }
}
```

<a name="handling-file-uploads"></a>
## ファイルのアップロードの処理 (Handling File Uploads)

デフォルトでは、Laravel Precognition は、事前認識検証リクエスト中にファイルをアップロードまたは検証しません。これにより、大きなファイルが不必要に複数回アップロードされることがなくなります。

この動作のため、フィールドを指定するアプリケーション [対応するフォームリクエストの検証ルールをカスタマイズします](#customizing-validation-rules) が完全なフォーム送信の場合にのみ必要であることを確認する必要があります。

```php
/**
 * Get the validation rules that apply to the request.
 *
 * @return array
 */
protected function rules()
{
    return [
        'avatar' => [
            ...$this->isPrecognitive() ? [] : ['required'],
            'image',
            'mimes:jpg,png',
            'dimensions:ratio=3/2',
        ],
        // ...
    ];
}
```

すべての検証リクエストにファイルを含めたい場合は、クライアント側のフォーム インスタンスで `validateFiles` 関数を呼び出すことができます。

```js
form.validateFiles();
```

<a name="managing-side-effects"></a>
## 副作用の管理 (Managing Side-Effects)

`HandlePrecognitiveRequests` ミドルウェアをルートに追加するときは、予測リクエスト中にスキップする必要がある他のミドルウェアに副作用があるかどうかを考慮する必要があります。

たとえば、各ユーザーがアプリケーションと行う「インタラクション」の合計数を増加させるミドルウェアがある場合でも、事前認識リクエストをインタラクションとしてカウントしたくない場合があります。これを実現するには、インタラクション数を増やす前に、リクエストの `isPrecognitive` メソッドをチェックします。

```php
<?php

namespace App\Http\Middleware;

use App\Facades\Interaction;
use Closure;
use Illuminate\Http\Request;

class InteractionMiddleware
{
    /**
     * Handle an incoming request.
     */
    public function handle(Request $request, Closure $next): mixed
    {
        if (! $request->isPrecognitive()) {
            Interaction::incrementFor($request->user());
        }

        return $next($request);
    }
}
```

<a name="testing"></a>
## テスト (Testing)

テストで事前認識リクエストを作成したい場合、Laravel の `TestCase` には、`Precognition` リクエストヘッダーを追加する `withPrecognition` ヘルパが含まれています。

さらに、予知的リクエストが成功したことを主張したい場合、たとえば検証エラーを返さなかった場合は、レスポンスで `assertSuccessfulPrecognition` メソッドを使用できます。

```php tab=Pest
it('validates registration form with precognition', function () {
    $response = $this->withPrecognition()
        ->post('/register', [
            'name' => 'Taylor Otwell',
        ]);

    $response->assertSuccessfulPrecognition();

    expect(User::count())->toBe(0);
});
```

```php tab=PHPUnit
public function test_it_validates_registration_form_with_precognition()
{
    $response = $this->withPrecognition()
        ->post('/register', [
            'name' => 'Taylor Otwell',
        ]);

    $response->assertSuccessfulPrecognition();
    $this->assertSame(0, User::count());
}
```

