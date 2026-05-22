# HTTPリダイレクト (HTTP Redirects)

- [リダイレクトの作成](#creating-redirects)
- [名前付きルートへのリダイレクト](#redirecting-named-routes)
- [コントローラアクションへのリダイレクト](#redirecting-controller-actions)
- [フラッシュされたセッション データによるリダイレクト](#redirecting-with-flashed-session-data)

<a name="creating-redirects"></a>
## リダイレクトの作成 (Creating Redirects)

リダイレクト応答は `Illuminate\Http\RedirectResponse` クラスのインスタンスであり、ユーザーを別の URL にリダイレクトするために必要な適切なヘッダーが含まれています。 `RedirectResponse` インスタンスを生成するには、いくつかの方法があります。最も簡単な方法は、グローバル `redirect` ヘルパを使用することです。

    Route::get('/dashboard', function () {
        return redirect('/home/dashboard');
    });

送信されたフォームが無効な場合など、ユーザーを以前の場所にリダイレクトしたい場合があります。これを行うには、グローバル `back` ヘルパ関数を使用します。この機能は [session](/docs/{{version}}/session) を利用するため、`back` 関数を呼び出すルートが `web` ミドルウェア グループを使用しているか、すべてのセッション ミドルウェアが適用されていることを確認してください。

    Route::post('/user/profile', function () {
        // Validate the request...

        return back()->withInput();
    });

<a name="redirecting-named-routes"></a>
## 名前付きルートへのリダイレクト (Redirecting To Named Routes)

パラメーターを指定せずに `redirect` ヘルパを呼び出すと、`Illuminate\Routing\Redirector` のインスタンスが返され、`Redirector` インスタンスの任意のメソッドを呼び出すことができます。たとえば、名前付きルートに `RedirectResponse` を生成するには、`route` メソッドを使用できます。

    return redirect()->route('login');

ルートにパラメーターがある場合は、それらを `route` メソッドの 2 番目の引数として渡すことができます。

    // For a route with the following URI: profile/{id}

    return redirect()->route('profile', ['id' => 1]);

便宜上、Laravel ではグローバル `to_route` 関数も提供しています。

    return to_route('profile', ['id' => 1]);

<a name="populating-parameters-via-eloquent-models"></a>
#### Eloquent モデルを介したパラメーターの入力

Eloquent モデルから設定されている「ID」パラメータを持つルートにリダイレクトしている場合は、モデル自体を渡すことができます。 ID は自動的に抽出されます。

    // For a route with the following URI: profile/{id}

    return redirect()->route('profile', [$user]);

ルート パラメーターに配置される値をカスタマイズしたい場合は、Eloquent モデルで `getRouteKey` メソッドをオーバーライドする必要があります。

    /**
     * Get the value of the model's route key.
     *
     * @return mixed
     */
    public function getRouteKey()
    {
        return $this->slug;
    }

<a name="redirecting-controller-actions"></a>
## コントローラアクションへのリダイレクト (Redirecting To Controller Actions)

[コントローラのアクション](/docs/{{version}}/controllers) へのリダイレクトを生成することもできます。これを行うには、コントローラとアクション名を `action` メソッドに渡します。

    use App\Http\Controllers\HomeController;

    return redirect()->action([HomeController::class, 'index']);

コントローラ ルートにパラメーターが必要な場合は、それらを `action` メソッドの 2 番目の引数として渡すことができます。

    return redirect()->action(
        [UserController::class, 'profile'], ['id' => 1]
    );

<a name="redirecting-with-flashed-session-data"></a>
## フラッシュされたセッション データによるリダイレクト (Redirecting With Flashed Session Data)

通常、新しい URL へのリダイレクトと [セッションにデータをフラッシュする](/docs/{{version}}/session#flash-data) は同時に行われます。通常、これはアクションが正常に実行された後で、成功メッセージをセッションにフラッシュするときに行われます。便宜上、`RedirectResponse` インスタンスを作成し、単一の滑らかなメソッド チェーンでセッションにデータをフラッシュすることができます。

    Route::post('/user/profile', function () {
        // Update the user's profile...

        return redirect('/dashboard')->with('status', 'Profile updated!');
    });

`RedirectResponse` インスタンスによって提供される `withInput` メソッドを使用して、ユーザーを新しい場所にリダイレクトする前に、現在のリクエストの入力データをセッションにフラッシュできます。入力がセッションにフラッシュされると、次のリクエスト中に簡単に [それを取得します](/docs/{{version}}/requests#retrieving-old-input) を実行できます。

    return back()->withInput();

ユーザーがリダイレクトされた後、[session](/docs/{{version}}/session) からフラッシュされたメッセージを表示できます。たとえば、[Blade 構文](/docs/{{version}}/blade) を使用すると、次のようになります。

    @if (session('status'))
        <div class="alert alert-success">
            {{ session('status') }}
        </div>
    @endif

