# 検証 (Validation)

- [Introduction](#introduction)
- [検証のクイックスタート](#validation-quickstart)
    - [ルートの定義](#quick-defining-the-routes)
    - [コントローラの作成](#quick-creating-the-controller)
    - [検証ロジックの作成](#quick-writing-the-validation-logic)
    - [検証エラーの表示](#quick-displaying-the-validation-errors)
    - [フォームの再入力](#repopulating-forms)
    - [オプションのフィールドに関する注意](#a-note-on-optional-fields)
- [フォームリクエストの検証](#form-request-validation)
    - [フォームリクエストの作成](#creating-form-requests)
    - [フォームリクエストの承認](#authorizing-form-requests)
    - [エラーメッセージのカスタマイズ](#customizing-the-error-messages)
    - [検証のための入力の準備](#preparing-input-for-validation)
- [バリデーターを手動で作成する](#manually-creating-validators)
    - [自動リダイレクト](#automatic-redirection)
    - [名前付きエラーバッグ](#named-error-bags)
    - [エラーメッセージのカスタマイズ](#manual-customizing-the-error-messages)
    - [検証後フック](#after-validation-hook)
- [検証された入力の使用](#working-with-validated-input)
- [エラーメッセージの処理](#working-with-error-messages)
    - [言語ファイルでのカスタム メッセージの指定](#specifying-custom-messages-in-language-files)
    - [言語ファイルでの属性の指定](#specifying-attribute-in-language-files)
    - [言語ファイルでの値の指定](#specifying-values-in-language-files)
- [利用可能な検証ルール](#available-validation-rules)
- [条件付きルールの追加](#conditionally-adding-rules)
- [配列の検証](#validating-arrays)
    - [未検証の配列キーの除外](#excluding-unvalidated-array-keys)
    - [ネストされた配列入力の検証](#validating-nested-array-input)
- [パスワードの検証](#validating-passwords)
- [カスタム検証ルール](#custom-validation-rules)
    - [ルールオブジェクトの使用](#using-rule-objects)
    - [クロージャの使用](#using-closures)
    - [暗黙のルール](#implicit-rules)

<a name="introduction"></a>
## 導入 (Introduction)

Laravel は、アプリケーションの受信データを検証するためのいくつかの異なるアプローチを提供します。すべての受信 HTTP リクエストで使用できる `validate` メソッドを使用するのが最も一般的です。ただし、他の検証アプローチについても説明します。

Laravel には、データに適用できる便利な検証ルールが幅広く含まれており、特定のデータベーステーブル内で値が一意であるかどうかを検証する機能も提供します。 Laravel のすべての検証機能を理解できるように、これらの検証ルールのそれぞれについて詳しく説明します。

<a name="validation-quickstart"></a>
## 検証のクイックスタート (Validation Quickstart)

Laravel の強力な検証機能について学ぶために、フォームを検証し、ユーザーにエラー メッセージを表示する完全な例を見てみましょう。この高レベルの概要を読むことで、Laravel を使用して受信リクエスト データを検証する方法について一般的に理解できるようになります。

<a name="quick-defining-the-routes"></a>
### ルートの定義

まず、`routes/web.php` ファイルに次のルートが定義されていると仮定します。

    use App\Http\Controllers\PostController;

    Route::get('/post/create', [PostController::class, 'create']);
    Route::post('/post', [PostController::class, 'store']);

`GET` ルートはユーザーが新しいブログ投稿を作成するためのフォームを表示し、`POST` ルートは新しいブログ投稿をデータベースに保存します。

<a name="quick-creating-the-controller"></a>
### コントローラの作成

次に、これらのルートへの受信リクエストを処理する単純なコントローラを見てみましょう。現時点では、`store` メソッドを空のままにしておきます。

    <?php

    namespace App\Http\Controllers;

    use App\Http\Controllers\Controller;
    use Illuminate\Http\Request;

    class PostController extends Controller
    {
        /**
         * Show the form to create a new blog post.
         *
         * @return \Illuminate\View\View
         */
        public function create()
        {
            return view('post.create');
        }

        /**
         * Store a new blog post.
         *
         * @param  \Illuminate\Http\Request  $request
         * @return \Illuminate\Http\Response
         */
        public function store(Request $request)
        {
            // Validate and store the blog post...
        }
    }

<a name="quick-writing-the-validation-logic"></a>
### 検証ロジックの作成

これで、新しいブログ投稿を検証するロジックを `store` メソッドに入力する準備が整いました。これを行うには、`Illuminate\Http\Request` オブジェクトによって提供される `validate` メソッドを使用します。検証ルールに合格すると、コードは通常どおりに実行され続けます。ただし、検証が失敗した場合は、`Illuminate\Validation\ValidationException` 例外がスローされ、適切なエラー応答が自動的にユーザーに返されます。

従来の HTTP リクエスト中に検証が失敗した場合、前の URL へのリダイレクト応答が生成されます。受信リクエストが XHR リクエストの場合、検証エラー メッセージを含む JSON レスポンスが返されます。

`validate` メソッドをより深く理解するために、`store` メソッドに戻りましょう。

    /**
     * Store a new blog post.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        $validated = $request->validate([
            'title' => 'required|unique:posts|max:255',
            'body' => 'required',
        ]);

        // The blog post is valid...
    }

ご覧のとおり、検証ルールは `validate` メソッドに渡されます。心配しないでください。使用可能な検証ルールはすべて [documented](#available-validation-rules) です。繰り返しますが、検証が失敗した場合は、適切な応答が自動的に生成されます。検証に合格すると、コントローラは通常どおりに実行を続けます。

あるいは、単一の `|` で区切られた文字列の代わりに、検証ルールをルールの配列として指定することもできます。

    $validatedData = $request->validate([
        'title' => ['required', 'unique:posts', 'max:255'],
        'body' => ['required'],
    ]);

さらに、`validateWithBag` メソッドを使用してリクエストを検証し、エラー メッセージを [名前付きエラーバッグ](#named-error-bags) 内に保存することもできます。

    $validatedData = $request->validateWithBag('post', [
        'title' => ['required', 'unique:posts', 'max:255'],
        'body' => ['required'],
    ]);

<a name="stopping-on-first-validation-failure"></a>
#### 最初の検証失敗時に停止する

最初の検証が失敗した後、属性に対する検証ルールの実行を停止したい場合があります。これを行うには、`bail` ルールを属性に割り当てます。

    $request->validate([
        'title' => 'bail|required|unique:posts|max:255',
        'body' => 'required',
    ]);

この例では、`title` 属性の `unique` ルールが失敗した場合、`max` ルールはチェックされません。ルールは割り当てられた順序で検証されます。

<a name="a-note-on-nested-attributes"></a>
#### ネストされた属性に関する注意

受信した HTTP リクエストに「ネストされた」フィールド データが含まれている場合は、「ドット」構文を使用して検証ルールでこれらのフィールドを指定できます。

    $request->validate([
        'title' => 'required|unique:posts|max:255',
        'author.name' => 'required',
        'author.description' => 'required',
    ]);

一方、フィールド名にリテラルのピリオドが含まれている場合は、ピリオドをバックスラッシュでエスケープすることで、これが「ドット」構文として解釈されるのを明示的に防ぐことができます。

    $request->validate([
        'title' => 'required|unique:posts|max:255',
        'v1\.0' => 'required',
    ]);

<a name="quick-displaying-the-validation-errors"></a>
### 検証エラーの表示

では、受信リクエストフィールドが指定された検証ルールを通過しない場合はどうなるでしょうか?前述したように、Laravel はユーザーを以前の場所に自動的にリダイレクトします。さらに、すべての検証エラーと [入力を要求する](/docs/{{version}}/requests#retrieving-old-input) は自動的に [セッションにフラッシュされました](/docs/{{version}}/session#flash-data) になります。

`$errors` 変数は、`web` ミドルウェア グループによって提供される `Illuminate\View\Middleware\ShareErrorsFromSession` ミドルウェアによって、アプリケーションのすべてのビューと共有されます。このミドルウェアを適用すると、`$errors` 変数が常にビューで使用できるようになり、都合よく、`$errors` 変数が常に定義されており、安全に使用できると想定できます。 `$errors` 変数は、`Illuminate\Support\MessageBag` のインスタンスになります。このオブジェクトの操作の詳細については、[ドキュメントを確認してください](#working-with-error-messages) を参照してください。

したがって、この例では、検証が失敗したときにユーザーはコントローラの `create` メソッドにリダイレクトされ、ビューにエラー メッセージを表示できるようになります。

```html
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
#### エラーメッセージのカスタマイズ

Laravel の組み込み検証ルールにはそれぞれエラー メッセージがあり、アプリケーションの `resources/lang/en/validation.php` ファイルにあります。このファイル内に、各検証ルールの変換エントリがあります。アプリケーションのニーズに基づいて、これらのメッセージを自由に変更または修正できます。

さらに、このファイルを別の翻訳言語ディレクトリにコピーして、アプリケーションの言語にメッセージを翻訳することもできます。 Laravel ローカリゼーションの詳細については、完全な [ローカリゼーションドキュメント](/docs/{{version}}/localization) を確認してください。

<a name="quick-xhr-requests-and-validation"></a>
#### XHR リクエストと検証

この例では、従来のフォームを使用してデータをアプリケーションに送信しました。ただし、多くのアプリケーションは、JavaScript を利用したフロントエンドから XHR リクエストを受け取ります。 XHRリクエスト中に`validate`メソッドを使用すると、Laravelはリダイレクト応答を生成しません。代わりに、Laravel はすべての検証エラーを含む JSON 応答を生成します。この JSON 応答は 422 HTTP ステータス コードとともに送信されます。

<a name="the-at-error-directive"></a>
#### `@error` ディレクティブ

`@error` [Blade](/docs/{{version}}/blade) ディレクティブを使用すると、特定の属性に検証エラー メッセージが存在するかどうかを迅速に判断できます。 `@error` ディレクティブ内で、`$message` 変数をエコーし​​てエラー メッセージを表示できます。

```html
<!-- /resources/views/post/create.blade.php -->

<label for="title">Post Title</label>

<input id="title" type="text" name="title" class="@error('title') is-invalid @enderror">

@error('title')
    <div class="alert alert-danger">{{ $message }}</div>
@enderror
```

[名前付きエラーバッグ](#named-error-bags) を使用している場合は、エラー バッグの名前を 2 番目の引数として `@error` ディレクティブに渡すことができます。

```html
<input ... class="@error('title', 'post') is-invalid @enderror">
```

<a name="repopulating-forms"></a>
### フォームの再入力

Laravel が検証エラーによりリダイレクト応答を生成すると、フレームワークは自動的に [すべてのリクエストの入力をセッションにフラッシュします](/docs/{{version}}/session#flash-data) を実行します。これは、次のリクエスト中に入力に簡単にアクセスし、ユーザーが送信しようとしたフォームに再入力できるようにするために行われます。

前のリクエストからフラッシュされた入力を取得するには、`Illuminate\Http\Request` のインスタンスで `old` メソッドを呼び出します。 `old` メソッドは、以前にフラッシュされた入力データを [session](/docs/{{version}}/session) から取得します。

    $title = $request->old('title');

Laravel は、グローバル `old` ヘルパも提供します。 [Blade テンプレート](/docs/{{version}}/blade) 内で古い入力を表示している場合は、`old` ヘルパを使用してフォームに再入力する方が便利です。指定されたフィールドに古い入力が存在しない場合は、`null` が返されます。

    <input type="text" name="title" value="{{ old('title') }}">

<a name="a-note-on-optional-fields"></a>
### オプションのフィールドに関する注意

デフォルトでは、Laravel にはアプリケーションのグローバルミドルウェアスタックに `TrimStrings` および `ConvertEmptyStringsToNull` ミドルウェアが含まれています。これらのミドルウェアは、`App\Http\Kernel` クラスによってスタックにリストされます。このため、バリデーターで `null` 値が無効であるとみなされたくない場合は、多くの場合、「オプション」リクエスト フィールドを `nullable` としてマークする必要があります。例えば：

    $request->validate([
        'title' => 'required|unique:posts|max:255',
        'body' => 'required',
        'publish_at' => 'nullable|date',
    ]);

この例では、`publish_at` フィールドが `null` または有効な日付表現のいずれかであることを指定しています。 `nullable` 修飾子がルール定義に追加されていない場合、バリデーターは `null` を無効な日付と見なします。

<a name="form-request-validation"></a>
## フォームリクエストの検証 (Form Request Validation)

<a name="creating-form-requests"></a>
### フォームリクエストの作成

より複雑な検証シナリオの場合は、「フォームリクエスト」を作成することもできます。フォームリクエストは、独自の検証および認可ロジックをカプセル化するカスタムリクエストクラスです。フォームリクエストクラスを作成するには、`make:request` Artisan CLI コマンドを使用できます。

    php artisan make:request StorePostRequest

生成されたフォーム要求クラスは、`app/Http/Requests` ディレクトリに配置されます。このディレクトリが存在しない場合は、`make:request` コマンドを実行すると作成されます。 Laravel によって生成された各フォームリクエストには、`authorize` と `rules` という 2 つのメソッドがあります。

ご想像のとおり、`authorize` メソッドは、現在認証されているユーザーがリクエストで表されるアクションを実行できるかどうかを判断する役割を果たし、一方、`rules` メソッドはリクエストのデータに適用する必要がある検証ルールを返します。

    /**
     * Get the validation rules that apply to the request.
     *
     * @return array
     */
    public function rules()
    {
        return [
            'title' => 'required|unique:posts|max:255',
            'body' => 'required',
        ];
    }

> {tip} `rules` メソッドのシグネチャ内で必要な依存関係をタイプヒントで指定できます。これらは、Laravel [サービスコンテナ](/docs/{{version}}/container) を通じて自動的に解決されます。

では、検証ルールはどのように評価されるのでしょうか?必要なのは、コントローラ メソッドでリクエストをタイプヒントすることだけです。受信したフォームリクエストはコントローラメソッドが呼び出される前に検証されます。つまり、コントローラに検証ロジックを複雑にする必要はありません。

    /**
     * Store a new blog post.
     *
     * @param  \App\Http\Requests\StorePostRequest  $request
     * @return Illuminate\Http\Response
     */
    public function store(StorePostRequest $request)
    {
        // The incoming request is valid...

        // Retrieve the validated input data...
        $validated = $request->validated();

        // Retrieve a portion of the validated input data...
        $validated = $request->safe()->only(['name', 'email']);
        $validated = $request->safe()->except(['name', 'email']);
    }

検証が失敗した場合は、ユーザーを以前の場所に戻すリダイレクト応答が生成されます。エラーはセッションにもフラッシュされるので、表示できるようになります。リクエストが XHR リクエストの場合、検証エラーの JSON 表現を含む 422 ステータス コードを含む HTTP 応答がユーザーに返されます。

<a name="adding-after-hooks-to-form-requests"></a>
#### フォームリクエストへのAfterフックの追加

フォームリクエストに「後」検証フックを追加したい場合は、`withValidator` メソッドを使用できます。このメソッドは完全に構築されたバリデータを受け取るため、検証ルールが実際に評価される前にそのメソッドのいずれかを呼び出すことができます。

    /**
     * Configure the validator instance.
     *
     * @param  \Illuminate\Validation\Validator  $validator
     * @return void
     */
    public function withValidator($validator)
    {
        $validator->after(function ($validator) {
            if ($this->somethingElseIsInvalid()) {
                $validator->errors()->add('field', 'Something is wrong with this field!');
            }
        });
    }


<a name="request-stopping-on-first-validation-rule-failure"></a>
#### 最初の検証失敗時の停止属性

リクエスト クラスに `stopOnFirstFailure` プロパティを追加することで、検証エラーが 1 回発生したらすべての属性の検証を停止するようバリデーターに通知できます。

    /**
     * Indicates if the validator should stop on the first rule failure.
     *
     * @var bool
     */
    protected $stopOnFirstFailure = true;

<a name="customizing-the-redirect-location"></a>
#### リダイレクト場所のカスタマイズ

前述したように、フォーム要求の検証が失敗した場合、ユーザーを以前の場所に戻すリダイレクト応答が生成されます。ただし、この動作は自由にカスタマイズできます。これを行うには、フォームリクエストで `$redirect` プロパティを定義します。

    /**
     * The URI that users should be redirected to if validation fails.
     *
     * @var string
     */
    protected $redirect = '/dashboard';

または、ユーザーを名前付きルートにリダイレクトしたい場合は、代わりに `$redirectRoute` プロパティを定義できます。

    /**
     * The route that users should be redirected to if validation fails.
     *
     * @var string
     */
    protected $redirectRoute = 'dashboard';

<a name="authorizing-form-requests"></a>
### フォームリクエストの承認

フォーム要求クラスには、`authorize` メソッドも含まれています。このメソッド内で、認証されたユーザーが実際に特定のリソースを更新する権限を持っているかどうかを判断できます。たとえば、ユーザーが更新しようとしているブログ コメントを実際に所有しているかどうかを判断できます。おそらく、次のメソッド内で [認可ゲートとポリシー](/docs/{{version}}/authorization) を操作することになります。

    use App\Models\Comment;

    /**
     * Determine if the user is authorized to make this request.
     *
     * @return bool
     */
    public function authorize()
    {
        $comment = Comment::find($this->route('comment'));

        return $comment && $this->user()->can('update', $comment);
    }

すべてのフォームリクエストは基本Laravelリクエストクラスを拡張するため、`user`メソッドを使用して現在認証されているユーザーにアクセスできます。また、上記の例の `route` メソッドの呼び出しにも注意してください。このメソッドを使用すると、以下の例の `{comment}` パラメーターなど、呼び出されるルートで定義された URI パラメーターへのアクセスが許可されます。

    Route::post('/comment/{comment}');

したがって、アプリケーションが [ルートモデルバインディング](/docs/{{version}}/routing#route-model-binding) を利用している場合は、リクエストのプロパティとして解決されたモデルにアクセスすることで、コードをさらに簡潔にすることができます。

    return $this->user()->can('update', $this->comment);

`authorize` メソッドが `false` を返した場合、403 ステータス コードを含む HTTP 応答が自動的に返され、コントローラ メソッドは実行されません。

アプリケーションの別の部分でリクエストの認可ロジックを処理する予定がある場合は、単に `authorize` メソッドから `true` を返すだけです。

    /**
     * Determine if the user is authorized to make this request.
     *
     * @return bool
     */
    public function authorize()
    {
        return true;
    }

> {tip} `authorize` メソッドのシグネチャ内で必要な依存関係をタイプヒントで指定できます。これらは、Laravel [サービスコンテナ](/docs/{{version}}/container) を通じて自動的に解決されます。

<a name="customizing-the-error-messages"></a>
### エラーメッセージのカスタマイズ

`messages` メソッドをオーバーライドすることで、フォーム リクエストで使用されるエラー メッセージをカスタマイズできます。このメソッドは、属性とルールのペアの配列と、それに対応するエラー メッセージを返す必要があります。

    /**
     * Get the error messages for the defined validation rules.
     *
     * @return array
     */
    public function messages()
    {
        return [
            'title.required' => 'A title is required',
            'body.required' => 'A message is required',
        ];
    }

<a name="customizing-the-validation-attributes"></a>
#### 検証属性のカスタマイズ

Laravel の組み込み検証ルールのエラー メッセージの多くには、`:attribute` プレースホルダーが含まれています。検証メッセージの `:attribute` プレースホルダーをカスタム属性名に置き換えたい場合は、`attributes` メソッドをオーバーライドしてカスタム名を指定できます。このメソッドは、属性と名前のペアの配列を返す必要があります。

    /**
     * Get custom attributes for validator errors.
     *
     * @return array
     */
    public function attributes()
    {
        return [
            'email' => 'email address',
        ];
    }

<a name="preparing-input-for-validation"></a>
### 検証のための入力の準備

検証ルールを適用する前にリクエストのデータを準備またはサニタイズする必要がある場合は、`prepareForValidation` メソッドを使用できます。

    use Illuminate\Support\Str;

    /**
     * Prepare the data for validation.
     *
     * @return void
     */
    protected function prepareForValidation()
    {
        $this->merge([
            'slug' => Str::slug($this->slug),
        ]);
    }

<a name="manually-creating-validators"></a>
## バリデーターを手動で作成する (Manually Creating Validators)

リクエストで `validate` メソッドを使用したくない場合は、`Validator` [facade](/docs/{{version}}/facades) を使用してバリデーター インスタンスを手動で作成できます。ファサードの `make` メソッドは、新しいバリデーター インスタンスを生成します。

    <?php

    namespace App\Http\Controllers;

    use App\Http\Controllers\Controller;
    use Illuminate\Http\Request;
    use Illuminate\Support\Facades\Validator;

    class PostController extends Controller
    {
        /**
         * Store a new blog post.
         *
         * @param  Request  $request
         * @return Response
         */
        public function store(Request $request)
        {
            $validator = Validator::make($request->all(), [
                'title' => 'required|unique:posts|max:255',
                'body' => 'required',
            ]);

            if ($validator->fails()) {
                return redirect('post/create')
                            ->withErrors($validator)
                            ->withInput();
            }

            // Retrieve the validated input...
            $validated = $validator->validated();

            // Retrieve a portion of the validated input...
            $validated = $validator->safe()->only(['name', 'email']);
            $validated = $validator->safe()->except(['name', 'email']);

            // Store the blog post...
        }
    }

`make` メソッドに渡される最初の引数は、検証対象のデータです。 2 番目の引数は、データに適用する必要がある検証ルールの配列です。

リクエストの検証が失敗したかどうかを確認した後、`withErrors` メソッドを使用してエラー メッセージをセッションにフラッシュできます。この方法を使用すると、リダイレクト後に `$errors` 変数がビューと自動的に共有されるため、ビューを簡単にユーザーに表示できるようになります。 `withErrors` メソッドは、バリデータ、`MessageBag`、または PHP `array` を受け入れます。

#### 最初の検証失敗時に停止する

`stopOnFirstFailure` メソッドは、検証エラーが 1 回発生すると、すべての属性の検証を停止する必要があることをバリデーターに通知します。

    if ($validator->stopOnFirstFailure()->fails()) {
        // ...
    }

<a name="automatic-redirection"></a>
### 自動リダイレクト

バリデーター インスタンスを手動で作成したいが、HTTP リクエストの `validate` メソッドによって提供される自動リダイレクトを利用したい場合は、既存のバリデーター インスタンスで `validate` メソッドを呼び出すことができます。検証が失敗した場合、ユーザーは自動的にリダイレクトされるか、XHR リクエストの場合は JSON レスポンスが返されます。

    Validator::make($request->all(), [
        'title' => 'required|unique:posts|max:255',
        'body' => 'required',
    ])->validate();

検証が失敗した場合は、`validateWithBag` メソッドを使用してエラー メッセージを [名前付きエラーバッグ](#named-error-bags) に保存できます。

    Validator::make($request->all(), [
        'title' => 'required|unique:posts|max:255',
        'body' => 'required',
    ])->validateWithBag('post');

<a name="named-error-bags"></a>
### 名前付きエラーバッグ

1 つのページに複数のフォームがある場合は、検証エラーを含む `MessageBag` に名前を付けると、特定のフォームのエラー メッセージを取得できるようになります。これを実現するには、2 番目の引数として名前を `withErrors` に渡します。

    return redirect('register')->withErrors($validator, 'login');

その後、`$errors` 変数から名前付き `MessageBag` インスタンスにアクセスできます。

    {{ $errors->login->first('email') }}

<a name="manual-customizing-the-error-messages"></a>
### エラーメッセージのカスタマイズ

必要に応じて、Laravel が提供するデフォルトのエラーメッセージの代わりに、バリデーターインスタンスが使用するカスタムエラーメッセージを提供できます。カスタム メッセージを指定するにはいくつかの方法があります。まず、カスタム メッセージを `Validator::make` メソッドの 3 番目の引数として渡すことができます。

    $validator = Validator::make($input, $rules, $messages = [
        'required' => 'The :attribute field is required.',
    ]);

この例では、`:attribute` プレースホルダーは、検証中のフィールドの実際の名前に置き換えられます。検証メッセージで他のプレースホルダーを利用することもできます。例えば：

    $messages = [
        'same' => 'The :attribute and :other must match.',
        'size' => 'The :attribute must be exactly :size.',
        'between' => 'The :attribute value :input is not between :min - :max.',
        'in' => 'The :attribute must be one of the following types: :values',
    ];

<a name="specifying-a-custom-message-for-a-given-attribute"></a>
#### 特定の属性に対するカスタム メッセージの指定

場合によっては、特定の属性に対してのみカスタム エラー メッセージを指定したい場合があります。 「ドット」表記を使用してこれを行うことができます。最初に属性の名前を指定し、次にルールを指定します。

    $messages = [
        'email.required' => 'We need to know your email address!',
    ];

<a name="specifying-custom-attribute-values"></a>
#### カスタム属性値の指定

Laravel の組み込みエラー メッセージの多くには、検証中のフィールドまたは属性の名前に置き換えられる `:attribute` プレースホルダーが含まれています。特定のフィールドのこれらのプレースホルダーを置換するために使用される値をカスタマイズするには、カスタム属性の配列を `Validator::make` メソッドの 4 番目の引数として渡すことができます。

    $validator = Validator::make($input, $rules, $messages, [
        'email' => 'email address',
    ]);

<a name="after-validation-hook"></a>
### 検証後フック

検証の完了後に実行されるコールバックをアタッチすることもできます。これにより、さらなる検証を簡単に実行でき、メッセージ コレクションにさらに多くのエラー メッセージを追加することもできます。まず、バリデーター インスタンスで `after` メソッドを呼び出します。

    $validator = Validator::make(...);

    $validator->after(function ($validator) {
        if ($this->somethingElseIsInvalid()) {
            $validator->errors()->add(
                'field', 'Something is wrong with this field!'
            );
        }
    });

    if ($validator->fails()) {
        //
    }

<a name="working-with-validated-input"></a>
## 検証された入力の使用 (Working With Validated Input)

フォームリクエストまたは手動で作成したバリデータインスタンスを使用して受信リクエストデータを検証した後、実際に検証を受けた受信リクエストデータを取得したい場合があります。これはいくつかの方法で実現できます。まず、フォームリクエストまたはバリデーターインスタンスで `validated` メソッドを呼び出すことができます。このメソッドは、検証されたデータの配列を返します。

    $validated = $request->validated();

    $validated = $validator->validated();

あるいは、フォームリクエストまたはバリデーターインスタンスで `safe` メソッドを呼び出すこともできます。このメソッドは、`Illuminate\Support\ValidatedInput` のインスタンスを返します。このオブジェクトは、検証済みデータのサブセットまたは検証済みデータの配列全体を取得するための `only`、`except`、および `all` メソッドを公開します。

    $validated = $request->safe()->only(['name', 'email']);

    $validated = $request->safe()->except(['name', 'email']);

    $validated = $request->safe()->all();

さらに、`Illuminate\Support\ValidatedInput` インスタンスは配列のように反復され、アクセスされる場合があります。

    // Validated data may be iterated...
    foreach ($request->safe() as $key => $value) {
        //
    }

    // Validated data may be accessed as an array...
    $validated = $request->safe();

    $email = $validated['email'];

検証されたデータにフィールドを追加したい場合は、`merge` メソッドを呼び出します。

    $validated = $request->safe()->merge(['name' => 'Taylor Otwell']);

検証されたデータを [collection](/docs/{{version}}/collections) インスタンスとして取得したい場合は、`collect` メソッドを呼び出します。

    $collection = $request->safe()->collect();

<a name="working-with-error-messages"></a>
## エラーメッセージの処理 (Working With Error Messages)

`Validator` インスタンスで `errors` メソッドを呼び出した後、エラー メッセージを処理するためのさまざまな便利なメソッドを備えた `Illuminate\Support\MessageBag` インスタンスを受け取ります。すべてのビューで自動的に使用可能になる `$errors` 変数も、`MessageBag` クラスのインスタンスです。

<a name="retrieving-the-first-error-message-for-a-field"></a>
#### フィールドの最初のエラー メッセージの取得

特定のフィールドの最初のエラー メッセージを取得するには、`first` メソッドを使用します。

    $errors = $validator->errors();

    echo $errors->first('email');

<a name="retrieving-all-error-messages-for-a-field"></a>
#### フィールドのすべてのエラー メッセージの取得

特定のフィールドのすべてのメッセージの配列を取得する必要がある場合は、`get` メソッドを使用します。

    foreach ($errors->get('email') as $message) {
        //
    }

配列フォーム フィールドを検証している場合は、`*` 文字を使用して、各配列要素のすべてのメッセージを取得できます。

    foreach ($errors->get('attachments.*') as $message) {
        //
    }

<a name="retrieving-all-error-messages-for-all-fields"></a>
#### すべてのフィールドのすべてのエラー メッセージを取得する

すべてのフィールドのすべてのメッセージの配列を取得するには、`all` メソッドを使用します。

    foreach ($errors->all() as $message) {
        //
    }

<a name="determining-if-messages-exist-for-a-field"></a>
#### フィールドにメッセージが存在するかどうかを確認する

`has` メソッドは、特定のフィールドにエラー メッセージが存在するかどうかを判断するために使用できます。

    if ($errors->has('email')) {
        //
    }

<a name="specifying-custom-messages-in-language-files"></a>
### 言語ファイルでのカスタム メッセージの指定

Laravel の組み込み検証ルールにはそれぞれエラー メッセージがあり、アプリケーションの `resources/lang/en/validation.php` ファイルにあります。このファイル内に、各検証ルールの変換エントリがあります。アプリケーションのニーズに基づいて、これらのメッセージを自由に変更または修正できます。

さらに、このファイルを別の翻訳言語ディレクトリにコピーして、アプリケーションの言語にメッセージを翻訳することもできます。 Laravel ローカリゼーションの詳細については、完全な [ローカリゼーションドキュメント](/docs/{{version}}/localization) を確認してください。

<a name="custom-messages-for-specific-attributes"></a>
#### 特定の属性のカスタム メッセージ

アプリケーションの検証言語ファイル内の指定された属性とルールの組み合わせに使用されるエラー メッセージをカスタマイズできます。これを行うには、アプリケーションの `resources/lang/xx/validation.php` 言語ファイルの `custom` 配列にメッセージのカスタマイズを追加します。

    'custom' => [
        'email' => [
            'required' => 'We need to know your email address!',
            'max' => 'Your email address is too long!'
        ],
    ],

<a name="specifying-attribute-in-language-files"></a>
### 言語ファイルでの属性の指定

Laravel の組み込みエラー メッセージの多くには、検証中のフィールドまたは属性の名前に置き換えられる `:attribute` プレースホルダーが含まれています。検証メッセージの `:attribute` 部分をカスタム値に置き換えたい場合は、`resources/lang/xx/validation.php` 言語ファイルの `attributes` 配列でカスタム属性名を指定できます。

    'attributes' => [
        'email' => 'email address',
    ],

<a name="specifying-values-in-language-files"></a>
### 言語ファイルでの値の指定

Laravel の組み込み検証ルールのエラー メッセージの一部には、リクエスト属性の現在の値に置き換えられる `:value` プレースホルダーが含まれています。ただし、検証メッセージの `:value` 部分を値のカスタム表現に置き換える必要がある場合があります。たとえば、`payment_type` の値が `cc` である場合にクレジット カード番号が必要であることを指定する次のルールを考えてみましょう。

    Validator::make($request->all(), [
        'credit_card_number' => 'required_if:payment_type,cc'
    ]);

この検証ルールが失敗すると、次のエラー メッセージが生成されます。

    The credit card number field is required when payment type is cc.

支払いタイプの値として `cc` を表示する代わりに、`values` 配列を定義することで、`resources/lang/xx/validation.php` 言語ファイルでよりユーザーフレンドリーな値表現を指定できます。

    'values' => [
        'payment_type' => [
            'cc' => 'credit card'
        ],
    ],

この値を定義すると、検証ルールによって次のエラー メッセージが生成されます。

    The credit card number field is required when payment type is credit card.

<a name="available-validation-rules"></a>
## 利用可能な検証ルール (Available Validation Rules)

以下は、利用可能なすべての検証ルールとその機能のリストです。

<style>
    .collection-method-list > p {
        column-count: 3; -moz-column-count: 3; -webkit-column-count: 3;
        column-gap: 2em; -moz-column-gap: 2em; -webkit-column-gap: 2em;
    }

    .collection-method-list a {
        display: block;
    }
</style>

<div class="collection-method-list" markdown="1">

[Accepted](#rule-accepted)
[受け入れられる場合](#rule-accepted-if)
[アクティブな URL](#rule-active-url)
[後 (日付)](#rule-after)
[以降 (日付)](#rule-after-or-equal)
[Alpha](#rule-alpha)
[アルファダッシュ](#rule-alpha-dash)
[英数字](#rule-alpha-num)
[Array](#rule-array)
[Bail](#rule-bail)
[前 (日付)](#rule-before)
[前または同じ (日付)](#rule-before-or-equal)
[Between](#rule-between)
[Boolean](#rule-boolean)
[Confirmed](#rule-confirmed)
[現在のパスワード](#rule-current-password)
[Date](#rule-date)
[日付が等しい](#rule-date-equals)
[日付形式](#rule-date-format)
[Declined](#rule-declined)
[拒否された場合](#rule-declined-if)
[Different](#rule-different)
[Digits](#rule-digits)
[間の数字](#rule-digits-between)
[寸法（画像ファイル）](#rule-dimensions)
[Distinct](#rule-distinct)
[Email](#rule-email)
[で終わる](#rule-ends-with)
[Enum](#rule-enum)
[Exclude](#rule-exclude)
[次の場合を除外する](#rule-exclude-if)
[次の場合を除きます](#rule-exclude-unless)
[除外せずに](#rule-exclude-without)
[存在します (データベース)](#rule-exists)
[File](#rule-file)
[Filled](#rule-filled)
[より大きい](#rule-gt)
[以上](#rule-gte)
[画像（ファイル）](#rule-image)
[In](#rule-in)
[配列内](#rule-in-array)
[Integer](#rule-integer)
[IPアドレス](#rule-ip)
[MACアドレス](#rule-mac)
[JSON](#rule-json)
[未満](#rule-lt)
[以下](#rule-lte)
[Max](#rule-max)
[MIME タイプ](#rule-mimetypes)
[ファイル拡張子別の MIME タイプ](#rule-mimes)
[Min](#rule-min)
[の倍数](#multiple-of)
[入っていない](#rule-not-in)
[正規表現ではありません](#rule-not-regex)
[Nullable](#rule-nullable)
[Numeric](#rule-numeric)
[Password](#rule-password)
[Present](#rule-present)
[Prohibited](#rule-prohibited)
[禁止されている場合](#rule-prohibited-if)
[以下の場合を除き禁止](#rule-prohibited-unless)
[Prohibits](#rule-prohibits)
[正規表現](#rule-regex)
[Required](#rule-required)
[必須の場合](#rule-required-if)
[例外的に必須](#rule-required-unless)
[必須](#rule-required-with)
[すべて必須](#rule-required-with-all)
[必須なし](#rule-required-without)
[すべてなしで必須](#rule-required-without-all)
[Same](#rule-same)
[Size](#rule-size)
[Sometimes](#validating-when-present)
[で始まる](#rule-starts-with)
[String](#rule-string)
[Timezone](#rule-timezone)
[ユニーク (データベース)](#rule-unique)
[URL](#rule-url)
[UUID](#rule-uuid)

</div>

<a name="rule-accepted"></a>
#### accepted

検証対象のフィールドは、`"yes"`、`"on"`、`1`、または `true` である必要があります。これは、「利用規約」への同意または同様のフィールドを検証するのに役立ちます。

<a name="rule-accepted-if"></a>
#### accepted_if:anotherfield,value,...

検証中の別のフィールドが指定された値と等しい場合、検証中のフィールドは `"yes"`、`"on"`、`1`、または `true` である必要があります。これは、「利用規約」への同意または同様のフィールドを検証するのに役立ちます。

<a name="rule-active-url"></a>
#### active_url

検証対象のフィールドには、`dns_get_record` PHP 関数に従って、有効な A または AAAA レコードが必要です。指定された URL のホスト名は、`dns_get_record` に渡される前に、`parse_url` PHP 関数を使用して抽出されます。

<a name="rule-after"></a>
#### after:_date_

検証対象のフィールドは、指定された日付以降の値である必要があります。日付は、有効な `DateTime` インスタンスに変換されるために、`strtotime` PHP 関数に渡されます。

    'start_date' => 'required|date|after:tomorrow'

`strtotime` によって評価される日付文字列を渡す代わりに、日付と比較する別のフィールドを指定できます。

    'finish_date' => 'required|date|after:start_date'

<a name="rule-after-or-equal"></a>
#### after\_or\_equal:_date_

検証対象のフィールドは、指定された日付以降の値である必要があります。詳細については、[after](#rule-after) ルールを参照してください。

<a name="rule-alpha"></a>
#### alpha

検証対象のフィールドは完全に英字である必要があります。

<a name="rule-alpha-dash"></a>
#### alpha_dash

検証中のフィールドには、英数字のほか、ダッシュやアンダースコアも使用できます。

<a name="rule-alpha-num"></a>
#### alpha_num

検証対象のフィールドは完全に英数字である必要があります。

<a name="rule-array"></a>
#### array

検証対象のフィールドは PHP `array` である必要があります。

追加の値が `array` ルールに指定される場合、入力配列内の各キーがルールに指定される値のリスト内に存在する必要があります。次の例では、入力配列の `admin` キーは、`array` ルールに提供される値のリストに含まれていないため、無効です。

    use Illuminate\Support\Facades\Validator;

    $input = [
        'user' => [
            'name' => 'Taylor Otwell',
            'username' => 'taylorotwell',
            'admin' => true,
        ],
    ];

    Validator::make($input, [
        'user' => 'array:username,locale',
    ]);

一般に、配列内に存在できる配列キーを常に指定する必要があります。それ以外の場合、バリデーターの `validate` メソッドと `validated` メソッドは、配列とそのすべてのキーを含む、検証されたすべてのデータを返します (それらのキーが他のネストされた配列検証ルールで検証されなかった場合でも)。

必要に応じて、許可されるキーのリストを指定せずに `array` ルールを使用する場合でも、返される「検証済み」データに未検証の配列キーを決して含めないように Laravel のバリデーターに指示することもできます。これを実現するには、アプリケーションの `AppServiceProvider` の `boot` メソッドでバリデーターの `excludeUnvalidatedArrayKeys` メソッドを呼び出すことができます。これを実行すると、バリデーターは、それらのキーが [ネストされた配列のルール](#validating-arrays) によって具体的に検証された場合にのみ、返される「検証済み」データに配列キーを含めます。

```php
use Illuminate\Support\Facades\Validator;

/**
 * Register any application services.
 *
 * @return void
 */
public function boot()
{
    Validator::excludeUnvalidatedArrayKeys();
}
```

<a name="rule-bail"></a>
#### bail

最初の検証が失敗した後は、フィールドの検証ルールの実行を停止します。

`bail` ルールは検証エラーが発生した場合にのみ特定のフィールドの検証を停止しますが、`stopOnFirstFailure` メソッドは、単一の検証エラーが発生するとすべての属性の検証を停止する必要があることをバリデーターに通知します。

    if ($validator->stopOnFirstFailure()->fails()) {
        // ...
    }

<a name="rule-before"></a>
#### before:_date_

検証対象のフィールドは、指定された日付より前の値である必要があります。日付は、有効な `DateTime` インスタンスに変換されるために、PHP `strtotime` 関数に渡されます。さらに、[`after`](#rule-after) ルールと同様に、検証中の別のフィールドの名前を `date` の値として指定することもできます。

<a name="rule-before-or-equal"></a>
#### before\_or\_equal:_date_

検証対象のフィールドは、指定された日付以前の値である必要があります。日付は、有効な `DateTime` インスタンスに変換されるために、PHP `strtotime` 関数に渡されます。さらに、[`after`](#rule-after) ルールと同様に、検証中の別のフィールドの名前を `date` の値として指定することもできます。

<a name="rule-between"></a>
#### between:_min_,_max_

検証対象のフィールドのサイズは、指定された _min_ と _max_ の間である必要があります。文字列、数値、配列、ファイルは、[`size`](#rule-size) ルールと同じ方法で評価されます。

<a name="rule-boolean"></a>
#### boolean

検証中のフィールドはブール値としてキャストできる必要があります。受け入れられる入力は、`true`、`false`、`1`、`0`、`"1"`、および `"0"` です。

<a name="rule-confirmed"></a>
#### confirmed

検証中のフィールドには、`{field}_confirmation` の一致するフィールドが必要です。たとえば、検証対象のフィールドが `password` の場合、一致する `password_confirmation` フィールドが入力に存在する必要があります。

<a name="rule-current-password"></a>
#### current_password

検証中のフィールドは、認証されたユーザーのパスワードと一致する必要があります。ルールの最初のパラメータを使用して、[認証ガード](/docs/{{version}}/authentication) を指定できます。

    'password' => 'current_password:api'

<a name="rule-date"></a>
#### date

検証対象のフィールドは、`strtotime` PHP 関数に従って、有効な非相対日付である必要があります。

<a name="rule-date-equals"></a>
#### date_equals:_date_

検証対象のフィールドは、指定された日付と一致する必要があります。日付は、有効な `DateTime` インスタンスに変換されるために、PHP `strtotime` 関数に渡されます。

<a name="rule-date-format"></a>
#### date_format:_format_

検証中のフィールドは、指定された _format_ と一致する必要があります。フィールドを検証するときは、`date` または `date_format` の両方ではなく、**どちらか** を使用する必要があります。この検証ルールは、PHP の [DateTime](https://www.php.net/manual/en/class.datetime.php) クラスでサポートされるすべての形式をサポートします。

<a name="rule-declined"></a>
#### declined

検証対象のフィールドは、`"no"`、`"off"`、`0`、または `false` である必要があります。

<a name="rule-declined-if"></a>
#### declined_if:anotherfield,value,...

検証中の別のフィールドが指定された値と等しい場合、検証中のフィールドは `"no"`、`"off"`、`0`、または `false` である必要があります。

<a name="rule-different"></a>
#### different:_field_

検証中のフィールドは、_field_ とは異なる値を持つ必要があります。

<a name="rule-digits"></a>
#### digits:_value_

検証対象のフィールドは _numeric_ であり、_value_ の正確な長さである必要があります。

<a name="rule-digits-between"></a>
#### digits_between:_min_,_max_

検証対象のフィールドは _numeric_ であり、指定された _min_ と _max_ の間の長さである必要があります。

<a name="rule-dimensions"></a>
#### dimensions

検証中のファイルは、ルールのパラメータで指定された寸法制約を満たす画像である必要があります。

    'avatar' => 'dimensions:min_width=100,min_height=200'

使用可能な制約は、_min\_width_、_max\_width_、_min\_height_、_max\_height_、_width_、_height_、_ratio_ です。

_ratio_ 制約は、幅を高さで割ったものとして表す必要があります。これは、`3/2` のような分数または `1.5` のような浮動小数点数のいずれかで指定できます。

    'avatar' => 'dimensions:ratio=3/2'

このルールには複数の引数が必要なため、`Rule::dimensions` メソッドを使用してルールをスムーズに構築できます。

    use Illuminate\Support\Facades\Validator;
    use Illuminate\Validation\Rule;

    Validator::make($data, [
        'avatar' => [
            'required',
            Rule::dimensions()->maxWidth(1000)->maxHeight(500)->ratio(3 / 2),
        ],
    ]);

<a name="rule-distinct"></a>
#### distinct

配列を検証する場合、検証対象のフィールドに重複する値があってはなりません。

    'foo.*.id' => 'distinct'

Distinct は、デフォルトで緩い変数比較を使用します。厳密な比較を使用するには、検証ルール定義に `strict` パラメータを追加します。

    'foo.*.id' => 'distinct:strict'

検証ルールの引数に `ignore_case` を追加して、大文字と小文字の違いをルールに無視させることができます。

    'foo.*.id' => 'distinct:ignore_case'

<a name="rule-email"></a>
#### email

検証中のフィールドは電子メール アドレスとしてフォーマットされている必要があります。この検証ルールは、電子メール アドレスを検証するために [`egulias/email-validator`](https://github.com/egulias/EmailValidator) パッケージを利用します。デフォルトでは、`RFCValidation` バリデーターが適用されますが、他の検証スタイルも適用できます。

    'email' => 'email:rfc,dns'

上記の例では、`RFCValidation` 検証と `DNSCheckValidation` 検証を適用します。適用できる検証スタイルの完全なリストは次のとおりです。

<div class="content-list" markdown="1">

- `rfc`: `RFCValidation`
- `strict`: `NoRFCWarningsValidation`
- `dns`: `DNSCheckValidation`
- `spoof`: `SpoofCheckValidation`
- `filter`: `FilterEmailValidation`

</div>

PHP の `filter_var` 関数を使用する `filter` バリデータは Laravel に同梱されており、Laravel バージョン 5.8 より前の Laravel のデフォルトの電子メール検証動作でした。

> {note} `dns` および `spoof` バリデーターには、PHP `intl` 拡張機能が必要です。

<a name="rule-ends-with"></a>
#### ends_with:_foo_,_bar_,...

検証中のフィールドは、指定された値のいずれかで終わる必要があります。

<a name="rule-enum"></a>
#### enum

`Enum` ルールは、検証対象のフィールドに有効な列挙値が含まれているかどうかを検証するクラス ベースのルールです。 `Enum` ルールは、列挙型の名前を唯一のコンストラクター引数として受け入れます。

    use App\Enums\ServerStatus;
    use Illuminate\Validation\Rules\Enum;

    $request->validate([
        'status' => [new Enum(ServerStatus::class)],
    ]);

> {note} 列挙型は PHP 8.1 以降でのみ使用できます。

<a name="rule-exclude"></a>
#### exclude

検証中のフィールドは、`validate` メソッドおよび `validated` メソッドによって返されるリクエスト データから除外されます。

<a name="rule-exclude-if"></a>
#### exclude_if:_anotherfield_,_value_

_anotherfield_ フィールドが _value_ と等しい場合、検証中のフィールドは、`validate` メソッドおよび `validated` メソッドによって返されるリクエスト データから除外されます。

<a name="rule-exclude-unless"></a>
#### exclude_unless:_anotherfield_,_value_

検証中のフィールドは、_anotherfield_ のフィールドが _value_ と等しい場合を除き、`validate` メソッドおよび `validated` メソッドによって返されるリクエスト データから除外されます。 _value_ が `null` (`exclude_unless:name,null`) の場合、比較フィールドが `null` でない限り、または比較フィールドがリクエスト データに欠落している場合を除き、検証対象のフィールドは除外されます。

<a name="rule-exclude-without"></a>
#### exclude_without:_anotherfield_

_anotherfield_ フィールドが存在しない場合、検証中のフィールドは、`validate` および `validated` メソッドによって返されるリクエスト データから除外されます。

<a name="rule-exists"></a>
#### exists:_table_,_column_

検証対象のフィールドは、特定のデータベース テーブルに存在する必要があります。

<a name="basic-usage-of-exists-rule"></a>
#### Exists ルールの基本的な使用法

    'state' => 'exists:states'

`column` オプションが指定されていない場合は、フィールド名が使用されます。したがって、この場合、ルールは、`states` データベース テーブルに、リクエストの `state` 属性値と一致する `state` 列値を持つレコードが含まれていることを検証します。

<a name="specifying-a-custom-column-name"></a>
#### カスタム列名の指定

データベーステーブル名の後に置くことで、検証ルールで使用するデータベース列名を明示的に指定できます。

    'state' => 'exists:states,abbreviation'

場合によっては、`exists` クエリに使用する特定のデータベース接続を指定する必要がある場合があります。これを行うには、テーブル名の前に接続名を追加します。

    'email' => 'exists:connection.staff,email'

テーブル名を直接指定する代わりに、テーブル名の決定に使用する Eloquent モデルを指定することもできます。

    'user_id' => 'exists:App\Models\User,id'

検証ルールによって実行されるクエリをカスタマイズしたい場合は、`Rule` クラスを使用してルールをスムーズに定義できます。この例では、検証ルールを `|` 文字で区切るのではなく、配列として指定します。

    use Illuminate\Support\Facades\Validator;
    use Illuminate\Validation\Rule;

    Validator::make($data, [
        'email' => [
            'required',
            Rule::exists('staff')->where(function ($query) {
                return $query->where('account_id', 1);
            }),
        ],
    ]);

<a name="rule-file"></a>
#### file

検証中のフィールドは、正常にアップロードされたファイルである必要があります。

<a name="rule-filled"></a>
#### filled

検証中のフィールドが存在する場合、空であってはなりません。

<a name="rule-gt"></a>
#### gt:_field_

検証対象のフィールドは、指定された _field_ より大きくなければなりません。 2 つのフィールドは同じタイプである必要があります。文字列、数値、配列、およびファイルは、[`size`](#rule-size) ルールと同じ規則を使用して評価されます。

<a name="rule-gte"></a>
#### gte:_field_

検証対象のフィールドは、指定された _field_ 以上である必要があります。 2 つのフィールドは同じタイプである必要があります。文字列、数値、配列、およびファイルは、[`size`](#rule-size) ルールと同じ規則を使用して評価されます。

<a name="rule-image"></a>
#### image

検証されるファイルは画像 (jpg、jpeg、png、bmp、gif、svg、または webp) である必要があります。

<a name="rule-in"></a>
#### in:_foo_,_bar_,...

検証中のフィールドは、指定された値のリストに含まれている必要があります。このルールでは配列を `implode` する必要があることが多いため、ルールをスムーズに構築するために `Rule::in` メソッドを使用できます。

    use Illuminate\Support\Facades\Validator;
    use Illuminate\Validation\Rule;

    Validator::make($data, [
        'zones' => [
            'required',
            Rule::in(['first-zone', 'second-zone']),
        ],
    ]);

`in` ルールを `array` ルールと組み合わせる場合、入力配列の各値は、`in` ルールに提供される値のリスト内に存在する必要があります。次の例では、入力配列の `LAS` 空港コードは、`in` ルールに指定された空港のリストに含まれていないため、無効です。

    use Illuminate\Support\Facades\Validator;
    use Illuminate\Validation\Rule;

    $input = [
        'airports' => ['NYC', 'LAS'],
    ];

    Validator::make($input, [
        'airports' => [
            'required',
            'array',
            Rule::in(['NYC', 'LIT']),
        ],
    ]);

<a name="rule-in-array"></a>
#### in_array:_anotherfield_.*

検証中のフィールドは、_anotherfield_ の値に存在する必要があります。

<a name="rule-integer"></a>
#### integer

検証対象のフィールドは整数である必要があります。

> {note} この検証ルールは、入力が「整数」変数タイプであることを検証するのではなく、入力が PHP の `FILTER_VALIDATE_INT` ルールで受け入れられるタイプであることのみを検証します。入力が数値であることを検証する必要がある場合は、このルールを [`numeric` 検証ルール](#rule-numeric) と組み合わせて使用​​してください。

<a name="rule-ip"></a>
#### ip

検証対象のフィールドは IP アドレスである必要があります。

<a name="ipv4"></a>
#### ipv4

検証対象のフィールドは IPv4 アドレスである必要があります。

<a name="ipv6"></a>
#### ipv6

検証対象のフィールドは IPv6 アドレスである必要があります。

<a name="rule-mac"></a>
#### mac_address

検証対象のフィールドは MAC アドレスである必要があります。

<a name="rule-json"></a>
#### json

検証対象のフィールドは有効な JSON 文字列である必要があります。

<a name="rule-lt"></a>
#### lt:_field_

検証対象のフィールドは、指定された _field_ より小さくなければなりません。 2 つのフィールドは同じタイプである必要があります。文字列、数値、配列、およびファイルは、[`size`](#rule-size) ルールと同じ規則を使用して評価されます。

<a name="rule-lte"></a>
#### lte:_field_

検証対象のフィールドは、指定された _field_ 以下である必要があります。 2 つのフィールドは同じタイプである必要があります。文字列、数値、配列、およびファイルは、[`size`](#rule-size) ルールと同じ規則を使用して評価されます。

<a name="rule-max"></a>
#### max:_value_

検証対象のフィールドは、最大 _value_ 以下である必要があります。文字列、数値、配列、ファイルは、[`size`](#rule-size) ルールと同じ方法で評価されます。

<a name="rule-mimetypes"></a>
#### mimetypes:_text/plain_,...

検証中のファイルは、指定された MIME タイプのいずれかに一致する必要があります。

    'video' => 'mimetypes:video/avi,video/mpeg,video/quicktime'

アップロードされたファイルの MIME タイプを判断するために、ファイルの内容が読み取られ、フレームワークは MIME タイプを推測しようとしますが、これはクライアントが提供した MIME タイプとは異なる場合があります。

<a name="rule-mimes"></a>
#### mimes:_foo_,_bar_,...

検証中のファイルは、リストされた拡張子のいずれかに対応する MIME タイプを持っている必要があります。

<a name="basic-usage-of-mime-rule"></a>
#### MIMEルールの基本的な使い方

    'photo' => 'mimes:jpg,bmp,png'

拡張子を指定するだけで済みますが、このルールは実際には、ファイルの内容を読み取り、その MIME タイプを推測することによってファイルの MIME タイプを検証します。 MIME タイプとそれに対応する拡張子の完全なリストは、次の場所にあります。

[https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types](https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types)

<a name="rule-min"></a>
#### min:_value_

検証中のフィールドには最小の _value_ が必要です。文字列、数値、配列、ファイルは、[`size`](#rule-size) ルールと同じ方法で評価されます。

<a name="multiple-of"></a>
#### multiple_of:_value_

検証対象のフィールドは、_value_ の倍数である必要があります。

> {note} `multiple_of` ルールを使用するには、[`bcmath` PHP 拡張機能](https://www.php.net/manual/en/book.bc.php) が必要です。

<a name="rule-not-in"></a>
#### not_in:_foo_,_bar_,...

検証中のフィールドは、指定された値のリストに含めてはなりません。 `Rule::notIn` メソッドを使用すると、ルールをスムーズに構築できます。

    use Illuminate\Validation\Rule;

    Validator::make($data, [
        'toppings' => [
            'required',
            Rule::notIn(['sprinkles', 'cherries']),
        ],
    ]);

<a name="rule-not-regex"></a>
#### not_regex:_pattern_

検証中のフィールドは、指定された正規表現と一致してはなりません。

内部的には、このルールは PHP `preg_match` 関数を使用します。指定されたパターンは、`preg_match` で必要とされるのと同じ形式に従っており、有効な区切り文字も含まれている必要があります。例: `'email' => 'not_regex:/^.+$/i'`。

> {note} `regex` / `not_regex` パターンを使用する場合、特に正規表現に `|` 文字が含まれている場合は、`|` 区切り文字を使用する代わりに配列を使用して検証ルールを指定する必要がある場合があります。

<a name="rule-nullable"></a>
#### nullable

検証中のフィールドは `null` である可能性があります。

<a name="rule-numeric"></a>
#### numeric

検証対象のフィールドは [numeric](https://www.php.net/manual/en/function.is-numeric.php) である必要があります。

<a name="rule-password"></a>
#### password

検証中のフィールドは、認証されたユーザーのパスワードと一致する必要があります。

> {note} このルールは、Laravel 9 で削除する目的で `current_password` に名前変更されました。代わりに [現在のパスワード](#rule-current-password) ルールを使用してください。

<a name="rule-present"></a>
#### present

検証中のフィールドは入力データに存在する必要がありますが、空であってもかまいません。

<a name="rule-prohibited"></a>
#### prohibited

検証中のフィールドは空であるか、存在しない必要があります。

<a name="rule-prohibited-if"></a>
#### prohibited_if:_anotherfield_,_value_,...

_anotherfield_ フィールドがいずれかの _value_ と等しい場合、検証対象のフィールドは空であるか、存在しない必要があります。

<a name="rule-prohibited-unless"></a>
#### prohibited_unless:_anotherfield_,_value_,...

_anotherfield_ フィールドがいずれかの _value_ と等しい場合を除き、検証対象のフィールドは空であるか、存在しない必要があります。

<a name="rule-prohibits"></a>
#### prohibits:_anotherfield_,...

検証中のフィールドが存在する場合、たとえ空であっても、_anotherfield_ のフィールドは存在できません。

<a name="rule-regex"></a>
#### regex:_pattern_

検証中のフィールドは、指定された正規表現と一致する必要があります。

内部的には、このルールは PHP `preg_match` 関数を使用します。指定されたパターンは、`preg_match` で必要とされるのと同じ形式に従っており、有効な区切り文字も含まれている必要があります。例: `'email' => 'regex:/^.+@.+$/i'`。

> {note} `regex` / `not_regex` パターンを使用する場合、特に正規表現に `|` 文字が含まれている場合は、`|` 区切り文字を使用する代わりに配列でルールを指定する必要がある場合があります。

<a name="rule-required"></a>
#### required

検証対象のフィールドは入力データに存在する必要があり、空であってはなりません。次の条件のいずれかが当てはまる場合、フィールドは「空」とみなされます。

<div class="content-list" markdown="1">

- 値は`null`です。
- 値は空の文字列です。
- 値は空の配列または空の `Countable` オブジェクトです。
- 値は、パスのないアップロードされたファイルです。

</div>

<a name="rule-required-if"></a>
#### required_if:_anotherfield_,_value_,...

_anotherfield_ フィールドがいずれかの _value_ と等しい場合、検証中のフィールドは存在する必要があり、空であってはなりません。

`required_if` ルールのより複雑な条件を作成したい場合は、`Rule::requiredIf` メソッドを使用できます。このメソッドはブール値またはクロージャを受け入れます。クロージャが渡されると、クロージャは `true` または `false` を返し、検証中のフィールドが必要かどうかを示す必要があります。

    use Illuminate\Support\Facades\Validator;
    use Illuminate\Validation\Rule;

    Validator::make($request->all(), [
        'role_id' => Rule::requiredIf($request->user()->is_admin),
    ]);

    Validator::make($request->all(), [
        'role_id' => Rule::requiredIf(function () use ($request) {
            return $request->user()->is_admin;
        }),
    ]);

<a name="rule-required-unless"></a>
#### required_unless:_anotherfield_,_value_,...

検証中のフィールドは存在する必要があり、_anotherfield_ フィールドがいずれかの _value_ と等しい場合を除き、空であってはなりません。これは、_value_ が `null` でない限り、_anotherfield_ がリクエスト データに存在する必要があることも意味します。 _value_ が `null` (`required_unless:name,null`) の場合、比較フィールドが `null` でない限り、または比較フィールドがリクエスト データに欠落している場合を除き、検証対象のフィールドが必要になります。

<a name="rule-required-with"></a>
#### required_with:_foo_,_bar_,...

検証対象のフィールドは、他の指定されたフィールドが存在し、空でない場合にのみ、存在し、空であってはなりません。

<a name="rule-required-with-all"></a>
#### required_with_all:_foo_,_bar_,...

検証対象のフィールドは、他の指定されたフィールドがすべて存在し、空でない場合にのみ、存在し、空であってはなりません。

<a name="rule-required-without"></a>
#### required_without:_foo_,_bar_,...

検証対象のフィールドは、指定された他のフィールドが空であるか存在しない場合にのみ、空ではなく存在する必要があります。

<a name="rule-required-without-all"></a>
#### required_without_all:_foo_,_bar_,...

検証対象のフィールドは、他の指定フィールドがすべて空であるか存在しない場合にのみ、空ではなく存在する必要があります。

<a name="rule-same"></a>
#### same:_field_

指定された _field_ は検証中のフィールドと一致する必要があります。

<a name="rule-size"></a>
#### size:_value_

検証中のフィールドのサイズは、指定された _value_ と一致する必要があります。文字列データの場合、_value_ は文字数に対応します。数値データの場合、_value_ は指定された整数値に対応します (属性には `numeric` または `integer` ルールも必要です)。配列の場合、_size_ は配列の `count` に対応します。ファイルの場合、_size_ はキロバイト単位のファイル サイズに対応します。いくつかの例を見てみましょう。

    // Validate that a string is exactly 12 characters long...
    'title' => 'size:12';

    // Validate that a provided integer equals 10...
    'seats' => 'integer|size:10';

    // Validate that an array has exactly 5 elements...
    'tags' => 'array|size:5';

    // Validate that an uploaded file is exactly 512 kilobytes...
    'image' => 'file|size:512';

<a name="rule-starts-with"></a>
#### starts_with:_foo_,_bar_,...

検証中のフィールドは、指定された値のいずれかで始まる必要があります。

<a name="rule-string"></a>
#### string

検証対象のフィールドは文字列である必要があります。フィールドを `null` にすることも許可したい場合は、フィールドに `nullable` ルールを割り当てる必要があります。

<a name="rule-timezone"></a>
#### timezone

検証対象のフィールドは、`timezone_identifiers_list` PHP 関数に従った有効なタイムゾーン識別子である必要があります。

<a name="rule-unique"></a>
#### unique:_table_,_column_

検証中のフィールドは、指定されたデータベース テーブル内に存在してはなりません。

**カスタム テーブル/列名の指定:**

テーブル名を直接指定する代わりに、テーブル名の決定に使用する Eloquent モデルを指定することもできます。

    'email' => 'unique:App\Models\User,email_address'

`column` オプションを使用して、フィールドに対応するデータベース列を指定できます。 `column` オプションが指定されていない場合は、検証中のフィールドの名前が使用されます。

    'email' => 'unique:users,email_address'

**カスタム データベース接続の指定**

場合によっては、バリデーターによって行われるデータベース クエリに対してカスタム接続を設定する必要がある場合があります。これを実現するには、テーブル名の前に接続名を追加します。

    'email' => 'unique:connection.users,email_address'

**特定の ID を無視するように固有のルールを強制する:**

場合によっては、一意の検証中に特定の ID を無視したい場合があります。たとえば、ユーザーの名前、電子メール アドレス、場所が含まれる「プロフィールの更新」画面を考えてみましょう。おそらく、電子メール アドレスが一意であることを確認する必要があるでしょう。ただし、ユーザーが名前フィールドのみを変更し、電子メール フィールドを変更しない場合、ユーザーはすでに問題の電子メール アドレスの所有者であるため、検証エラーがスローされることは望ましくありません。

ユーザーの ID を無視するようにバリデーターに指示するには、`Rule` クラスを使用してルールをスムーズに定義します。この例では、ルールを区切るために `|` 文字を使用する代わりに、検証ルールを配列として指定します。

    use Illuminate\Support\Facades\Validator;
    use Illuminate\Validation\Rule;

    Validator::make($data, [
        'email' => [
            'required',
            Rule::unique('users')->ignore($user->id),
        ],
    ]);

> {note} ユーザー制御のリクエスト入力を `ignore` メソッドに渡さないでください。代わりに、Eloquent モデル インスタンスからの自動インクリメント ID や UUID など、システムが生成した一意の ID のみを渡す必要があります。そうしないと、アプリケーションが SQL インジェクション攻撃に対して脆弱になります。

モデル キーの値を `ignore` メソッドに渡す代わりに、モデル インスタンス全体を渡すこともできます。 Laravel はモデルからキーを自動的に抽出します。

    Rule::unique('users')->ignore($user)

テーブルで `id` 以外の主キー列名を使用する場合は、`ignore` メソッドを呼び出すときに列の名前を指定できます。

    Rule::unique('users')->ignore($user->id, 'user_id')

デフォルトでは、`unique` ルールは、検証される属性の名前に一致する列の一意性をチェックします。ただし、別の列名を `unique` メソッドの 2 番目の引数として渡すこともできます。

    Rule::unique('users', 'email_address')->ignore($user->id),

**Where 句を追加する:**

`where` メソッドを使用してクエリをカスタマイズすることにより、追加のクエリ条件を指定できます。たとえば、`account_id` 列の値が `1` であるレコードのみを検索するようにクエリの範囲を設定するクエリ条件を追加してみましょう。

    'email' => Rule::unique('users')->where(function ($query) {
        return $query->where('account_id', 1);
    })

<a name="rule-url"></a>
#### url

検証対象のフィールドは有効な URL である必要があります。

<a name="rule-uuid"></a>
#### uuid

検証対象のフィールドは、有効な RFC 4122 (バージョン 1、3、4、または 5) の汎用一意識別子 (UUID) である必要があります。

<a name="conditionally-adding-rules"></a>
## 条件付きルールの追加 (Conditionally Adding Rules)

<a name="skipping-validation-when-fields-have-certain-values"></a>
#### フィールドに特定の値がある場合の検証のスキップ

別のフィールドに特定の値がある場合、特定のフィールドを検証したくない場合があります。これは、`exclude_if` 検証ルールを使用して実行できます。この例では、`has_appointment` フィールドの値が `false` である場合、`appointment_date` フィールドと `doctor_name` フィールドは検証されません。

    use Illuminate\Support\Facades\Validator;

    $validator = Validator::make($data, [
        'has_appointment' => 'required|boolean',
        'appointment_date' => 'exclude_if:has_appointment,false|required|date',
        'doctor_name' => 'exclude_if:has_appointment,false|required|string',
    ]);

あるいは、`exclude_unless` ルールを使用して、別のフィールドに特定の値がない限り、特定のフィールドを検証しないこともできます。

    $validator = Validator::make($data, [
        'has_appointment' => 'required|boolean',
        'appointment_date' => 'exclude_unless:has_appointment,true|required|date',
        'doctor_name' => 'exclude_unless:has_appointment,true|required|string',
    ]);

<a name="validating-when-present"></a>
#### 存在する場合の検証

状況によっては、フィールドが検証対象のデータに存在する場合にのみ**、そのフィールドに対して検証チェックを実行したい場合があります。これをすばやく実行するには、`sometimes` ルールをルール リストに追加します。

    $v = Validator::make($data, [
        'email' => 'sometimes|required|email',
    ]);

上記の例では、`email` フィールドは、`$data` 配列に存在する場合にのみ検証されます。

> {tip} 常に存在する必要があるフィールドが空である可能性があることを検証しようとしている場合は、[このメモはオプションのフィールドに関するものです](#a-note-on-optional-fields) を確認してください。

<a name="complex-conditional-validation"></a>
#### 複雑な条件付き検証

場合によっては、より複雑な条件ロジックに基づいた検証ルールを追加したい場合があります。たとえば、別のフィールドの値が 100 より大きい場合にのみ、特定のフィールドを必須にすることができます。または、別のフィールドが存在する場合にのみ、2 つのフィールドに特定の値を設定する必要がある場合があります。これらの検証ルールの追加は、それほど難しいことではありません。まず、決して変更されない_静的ルール_を使用して `Validator` インスタンスを作成します。

    use Illuminate\Support\Facades\Validator;

    $validator = Validator::make($request->all(), [
        'email' => 'required|email',
        'games' => 'required|numeric',
    ]);

Web アプリケーションがゲーム コレクター向けであると仮定しましょう。ゲームコレクターが当社のアプリケーションに登録し、100 以上のゲームを所有している場合、なぜそんなに多くのゲームを所有しているのか説明してもらいたいと考えています。たとえば、ゲームの再販ショップを経営しているかもしれませんし、単にゲームを収集するのが趣味かもしれません。この要件を条件付きで追加するには、`Validator` インスタンスで `sometimes` メソッドを使用します。

    $validator->sometimes('reason', 'required|max:500', function ($input) {
        return $input->games >= 100;
    });

`sometimes` メソッドに渡される最初の引数は、条件付きで検証するフィールドの名前です。 2 番目の引数は、追加するルールのリストです。 3 番目の引数として渡されたクロージャが `true` を返す場合、ルールが追加されます。この方法を使用すると、複雑な条件付き検証を簡単に構築できます。複数のフィールドの条件付き検証を一度に追加することもできます。

    $validator->sometimes(['reason', 'cost'], 'required', function ($input) {
        return $input->games >= 100;
    });

> {tip} クロージャに渡される `$input` パラメータは `Illuminate\Support\Fluent` のインスタンスとなり、検証中の入力やファイルにアクセスするために使用される場合があります。

<a name="complex-conditional-array-validation"></a>
#### 複雑な条件付き配列の検証

同じ入れ子配列内のインデックスが不明な別のフィールドに基づいてフィールドを検証したい場合があります。このような状況では、クロージャが検証中の配列内の現在の個々の項目となる 2 番目の引数を受け取ることを許可できます。

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

    $validator->sometimes('channels.*.address', 'email', function ($input, $item) {
        return $item->type === 'email';
    });

    $validator->sometimes('channels.*.address', 'url', function ($input, $item) {
        return $item->type !== 'email';
    });

クロージャに渡される `$input` パラメータと同様、属性データが配列の場合、`$item` パラメータは `Illuminate\Support\Fluent` のインスタンスになります。それ以外の場合は文字列です。

<a name="validating-arrays"></a>
## 配列の検証 (Validating Arrays)

[`array` 検証ルールのドキュメント](#rule-array) で説明したように、`array` ルールは、許可された配列キーのリストを受け入れます。配列内に追加のキーが存在する場合、検証は失敗します。

    use Illuminate\Support\Facades\Validator;

    $input = [
        'user' => [
            'name' => 'Taylor Otwell',
            'username' => 'taylorotwell',
            'admin' => true,
        ],
    ];

    Validator::make($input, [
        'user' => 'array:username,locale',
    ]);

一般に、配列内に存在できる配列キーを常に指定する必要があります。それ以外の場合、バリデーターの `validate` メソッドと `validated` メソッドは、配列とそのすべてのキーを含む、検証されたすべてのデータを返します (それらのキーが他のネストされた配列検証ルールで検証されなかった場合でも)。

<a name="excluding-unvalidated-array-keys"></a>
### 未検証の配列キーの除外

必要に応じて、許可されるキーのリストを指定せずに `array` ルールを使用する場合でも、返される「検証済み」データに未検証の配列キーを決して含めないように Laravel のバリデーターに指示することもできます。これを実現するには、アプリケーションの `AppServiceProvider` の `boot` メソッドでバリデーターの `excludeUnvalidatedArrayKeys` メソッドを呼び出すことができます。これを実行すると、バリデーターは、それらのキーが [ネストされた配列のルール](#validating-arrays) によって具体的に検証された場合にのみ、返される「検証済み」データに配列キーを含めます。

```php
use Illuminate\Support\Facades\Validator;

/**
 * Register any application services.
 *
 * @return void
 */
public function boot()
{
    Validator::excludeUnvalidatedArrayKeys();
}
```

<a name="validating-nested-array-input"></a>
### ネストされた配列入力の検証

ネストされた配列ベースのフォーム入力フィールドの検証は、それほど面倒なことではありません。 「ドット表記」を使用して、配列内の属性を検証できます。たとえば、受信した HTTP リクエストに `photos[profile]` フィールドが含まれている場合、次のように検証できます。

    use Illuminate\Support\Facades\Validator;

    $validator = Validator::make($request->all(), [
        'photos.profile' => 'required|image',
    ]);

配列の各要素を検証することもできます。たとえば、特定の配列入力フィールド内の各電子メールが一意であることを検証するには、次の手順を実行します。

    $validator = Validator::make($request->all(), [
        'person.*.email' => 'email|unique:users',
        'person.*.first_name' => 'required_with:person.*.last_name',
    ]);

同様に、[言語ファイル内のカスタム検証メッセージ](#custom-messages-for-specific-attributes) を指定するときに `*` 文字を使用すると、配列ベースのフィールドに対して単一の検証メッセージを簡単に使用できるようになります。

    'custom' => [
        'person.*.email' => [
            'unique' => 'Each person must have a unique email address',
        ]
    ],

<a name="validating-passwords"></a>
## パスワードの検証 (Validating Passwords)

パスワードに適切なレベルの複雑さを持たせるには、Laravel の `Password` ルール オブジェクトを使用できます。

    use Illuminate\Support\Facades\Validator;
    use Illuminate\Validation\Rules\Password;

    $validator = Validator::make($request->all(), [
        'password' => ['required', 'confirmed', Password::min(8)],
    ]);

`Password` ルール オブジェクトを使用すると、パスワードに少なくとも 1 つの文字、数字、記号、または大文字と小文字が混在する文字が必要であることを指定するなど、アプリケーションのパスワードの複雑さの要件を簡単にカスタマイズできます。

    // Require at least 8 characters...
    Password::min(8)

    // Require at least one letter...
    Password::min(8)->letters()

    // Require at least one uppercase and one lowercase letter...
    Password::min(8)->mixedCase()

    // Require at least one number...
    Password::min(8)->numbers()

    // Require at least one symbol...
    Password::min(8)->symbols()

さらに、`uncompromised` メソッドを使用して、パブリック パスワード データ漏洩でパスワードが侵害されていないことを確認できます。

    Password::min(8)->uncompromised()

内部的には、`Password` ルール オブジェクトは [k-Anonymity](https://en.wikipedia.org/wiki/K-anonymity) モデルを使用して、ユーザーのプライバシーやセキュリティを犠牲にすることなく、パスワードが [haveibeenpwned.com](https://haveibeenpwned.com) サービス経由で漏洩したかどうかを判断します。

デフォルトでは、パスワードがデータ漏洩の際に少なくとも 1 回出現すると、そのパスワードは侵害されたとみなされます。このしきい値は、`uncompromised` メソッドの最初の引数を使用してカスタマイズできます。

    // Ensure the password appears less than 3 times in the same data leak...
    Password::min(8)->uncompromised(3);

もちろん、上記の例のすべてのメソッドを連鎖させることもできます。

    Password::min(8)
        ->letters()
        ->mixedCase()
        ->numbers()
        ->symbols()
        ->uncompromised()

<a name="defining-default-password-rules"></a>
#### デフォルトのパスワードルールの定義

アプリケーションの単一の場所でパスワードのデフォルトの検証ルールを指定すると便利な場合があります。これは、クロージャを受け入れる `Password::defaults` メソッドを使用して簡単に実現できます。 `defaults` メソッドに指定されたクロージャは、パスワード ルールのデフォルト設定を返す必要があります。通常、`defaults` ルールは、アプリケーションのサービスプロバイダの 1 つの `boot` メソッド内で呼び出す必要があります。

```php
use Illuminate\Validation\Rules\Password;

/**
 * Bootstrap any application services.
 *
 * @return void
 */
public function boot()
{
    Password::defaults(function () {
        $rule = Password::min(8);

        return $this->app->isProduction()
                    ? $rule->mixedCase()->uncompromised()
                    : $rule;
    });
}
```

次に、検証中の特定のパスワードにデフォルトのルールを適用したい場合は、引数なしで `defaults` メソッドを呼び出すことができます。

    'password' => ['required', Password::defaults()],

場合によっては、デフォルトのパスワード検証ルールに追加の検証ルールを追加することが必要になる場合があります。これを実現するには、`rules` メソッドを使用できます。

    use App\Rules\ZxcvbnRule;

    Password::defaults(function () {
        $rule = Password::min(8)->rules([new ZxcvbnRule]);

        // ...
    });

<a name="custom-validation-rules"></a>
## カスタム検証ルール (Custom Validation Rules)

<a name="using-rule-objects"></a>
### ルールオブジェクトの使用

Laravel は、さまざまな便利な検証ルールを提供します。ただし、独自のものを指定したい場合もあります。カスタム検証ルールを登録する 1 つの方法は、ルール オブジェクトを使用することです。新しいルール オブジェクトを生成するには、`make:rule` Artisan コマンドを使用できます。このコマンドを使用して、文字列が大文字であることを検証するルールを生成してみましょう。 Laravel は新しいルールを `app/Rules` ディレクトリに配置します。このディレクトリが存在しない場合、Artisan コマンドを実行してルールを作成すると、Laravel によってディレクトリが作成されます。

    php artisan make:rule Uppercase

ルールを作成したら、その動作を定義する準備が整います。ルール オブジェクトには、`passes` と `message` の 2 つのメソッドが含まれています。 `passes` メソッドは属性値と名前を受け取り、属性値が有効かどうかに応じて `true` または `false` を返す必要があります。 `message` メソッドは、検証が失敗した場合に使用される検証エラー メッセージを返す必要があります。

    <?php

    namespace App\Rules;

    use Illuminate\Contracts\Validation\Rule;

    class Uppercase implements Rule
    {
        /**
         * Determine if the validation rule passes.
         *
         * @param  string  $attribute
         * @param  mixed  $value
         * @return bool
         */
        public function passes($attribute, $value)
        {
            return strtoupper($value) === $value;
        }

        /**
         * Get the validation error message.
         *
         * @return string
         */
        public function message()
        {
            return 'The :attribute must be uppercase.';
        }
    }

翻訳ファイルからエラー メッセージを返したい場合は、`message` メソッドから `trans` ヘルパを呼び出すことができます。

    /**
     * Get the validation error message.
     *
     * @return string
     */
    public function message()
    {
        return trans('validation.uppercase');
    }

ルールを定義したら、他の検証ルールとともにルール オブジェクトのインスタンスを渡すことで、ルールをバリデーターに添付できます。

    use App\Rules\Uppercase;

    $request->validate([
        'name' => ['required', 'string', new Uppercase],
    ]);

#### 追加データへのアクセス

カスタム検証ルール クラスが検証中の他のすべてのデータにアクセスする必要がある場合、ルール クラスは `Illuminate\Contracts\Validation\DataAwareRule` インターフェイスを実装できます。このインターフェイスでは、クラスで `setData` メソッドを定義する必要があります。このメソッドは、検証中のすべてのデータを使用して、Laravel によって (検証が続行する前に) 自動的に呼び出されます。

    <?php

    namespace App\Rules;

    use Illuminate\Contracts\Validation\Rule;
    use Illuminate\Contracts\Validation\DataAwareRule;

    class Uppercase implements Rule, DataAwareRule
    {
        /**
         * All of the data under validation.
         *
         * @var array
         */
        protected $data = [];

        // ...

        /**
         * Set the data under validation.
         *
         * @param  array  $data
         * @return $this
         */
        public function setData($data)
        {
            $this->data = $data;

            return $this;
        }
    }

または、検証ルールで検証を実行するバリデーター インスタンスへのアクセスが必要な場合は、`ValidatorAwareRule` インターフェイスを実装できます。

    <?php

    namespace App\Rules;

    use Illuminate\Contracts\Validation\Rule;
    use Illuminate\Contracts\Validation\ValidatorAwareRule;

    class Uppercase implements Rule, ValidatorAwareRule
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
         *
         * @param  \Illuminate\Validation\Validator  $validator
         * @return $this
         */
        public function setValidator($validator)
        {
            $this->validator = $validator;

            return $this;
        }
    }

<a name="using-closures"></a>
### クロージャの使用

アプリケーション全体でカスタム ルールの機能が 1 回だけ必要な場合は、ルール オブジェクトの代わりにクロージャを使用できます。クロージャは、属性の名前、属性の値、および検証が失敗した場合に呼び出される `$fail` コールバックを受け取ります。

    use Illuminate\Support\Facades\Validator;

    $validator = Validator::make($request->all(), [
        'title' => [
            'required',
            'max:255',
            function ($attribute, $value, $fail) {
                if ($value === 'foo') {
                    $fail('The '.$attribute.' is invalid.');
                }
            },
        ],
    ]);

<a name="implicit-rules"></a>
### 暗黙のルール

デフォルトでは、検証対象の属性が存在しないか、空の文字列が含まれている場合、カスタム ルールを含む通常の検証ルールは実行されません。たとえば、[`unique`](#rule-unique) ルールは空の文字列に対しては実行されません。

    use Illuminate\Support\Facades\Validator;

    $rules = ['name' => 'unique:users,name'];

    $input = ['name' => ''];

    Validator::make($input, $rules)->passes(); // true

属性が空の場合でもカスタム ルールを実行するには、その属性が必須であることをルールで暗黙的に示す必要があります。 「暗黙的な」ルールを作成するには、`Illuminate\Contracts\Validation\ImplicitRule` インターフェイスを実装します。このインターフェイスは、バリデーターの「マーカー インターフェイス」として機能します。したがって、一般的な `Rule` インターフェイスで必要なメソッド以外に実装する必要がある追加のメソッドは含まれていません。

新しい暗黙的なルール オブジェクトを生成するには、`make:rule` Artisan コマンドを `--implicit` オプションとともに使用します。

     php artisan make:rule Uppercase --implicit

> {note} 「暗黙的な」ルールは、属性が必須であることを_暗黙的に示すだけです。欠落している属性または空の属性を実際に無効にするかどうかは、ユーザー次第です。

