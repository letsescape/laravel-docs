<!-- # HTTP Redirects -->
# HTTP Redirects

- [Creating Redirects](#creating-redirects)
- [Redirecting To Named Routes](#redirecting-named-routes)
- [Redirecting To Controller Actions](#redirecting-controller-actions)
- [Redirecting With Flashed Session Data](#redirecting-with-flashed-session-data)

<a name="creating-redirects"></a>
<!-- ## Creating Redirects -->
## Creating Redirects

<!-- Redirect responses are instances of the `Illuminate\Http\RedirectResponse` class, and contain the proper headers needed to redirect the user to another URL. There are several ways to generate a `RedirectResponse` instance. The simplest method is to use the global `redirect` helper: -->
リダイレクト応答は `Illuminate\Http\RedirectResponse` クラスのインスタンスであり、ユーザーを別の URL にリダイレクトするために必要な適切なヘッダーが含まれています。 `RedirectResponse` インスタンスを生成するには、いくつかの方法があります。最も簡単な方法は、グローバル `redirect` ヘルパを使用することです。

```
Route::get('/dashboard', function () {
    return redirect('/home/dashboard');
});
```

<!-- Sometimes you may wish to redirect the user to their previous location, such as when a submitted form is invalid. You may do so by using the global `back` helper function. Since this feature utilizes the [session](/docs/8.x/session), make sure the route calling the `back` function is using the `web` middleware group or has all of the session middleware applied: -->
送信されたフォームが無効な場合など、ユーザーを以前の場所にリダイレクトしたい場合があります。これを行うには、グローバル `back` ヘルパ関数を使用します。この機能は [session](/docs/8.x/session) を利用するため、`back` 関数を呼び出すルートが `web` ミドルウェア グループを使用しているか、すべてのセッション ミドルウェアが適用されていることを確認してください。

```
Route::post('/user/profile', function () {
    // Validate the request...

    return back()->withInput();
});
```

<a name="redirecting-named-routes"></a>
<!-- ## Redirecting To Named Routes -->
## Redirecting To Named Routes

<!-- When you call the `redirect` helper with no parameters, an instance of `Illuminate\Routing\Redirector` is returned, allowing you to call any method on the `Redirector` instance. For example, to generate a `RedirectResponse` to a named route, you may use the `route` method: -->
パラメーターを指定せずに `redirect` ヘルパを呼び出すと、`Illuminate\Routing\Redirector` のインスタンスが返され、`Redirector` インスタンスの任意のメソッドを呼び出すことができます。たとえば、名前付きルートに `RedirectResponse` を生成するには、`route` メソッドを使用できます。

```
return redirect()->route('login');
```

<!-- If your route has parameters, you may pass them as the second argument to the `route` method: -->
ルートにパラメーターがある場合は、それらを `route` メソッドの 2 番目の引数として渡すことができます。

```
// For a route with the following URI: profile/{id}

return redirect()->route('profile', ['id' => 1]);
```

<a name="populating-parameters-via-eloquent-models"></a>
<!-- #### Populating Parameters Via Eloquent Models -->
#### Populating Parameters Via Eloquent Models

<!-- If you are redirecting to a route with an "ID" parameter that is being populated from an Eloquent model, you may pass the model itself. The ID will be extracted automatically: -->
Eloquent モデルから設定されている「ID」パラメータを持つルートにリダイレクトしている場合は、モデル自体を渡すことができます。 ID は自動的に抽出されます。

```
// For a route with the following URI: profile/{id}

return redirect()->route('profile', [$user]);
```

<!-- If you would like to customize the value that is placed in the route parameter, you should override the `getRouteKey` method on your Eloquent model: -->
ルート パラメーターに配置される値をカスタマイズしたい場合は、Eloquent モデルで `getRouteKey` メソッドをオーバーライドする必要があります。

```
/**
 * Get the value of the model's route key.
 *
 * @return mixed
 */
public function getRouteKey()
{
    return $this->slug;
}
```

<a name="redirecting-controller-actions"></a>
<!-- ## Redirecting To Controller Actions -->
## Redirecting To Controller Actions

<!-- You may also generate redirects to [controller actions](/docs/8.x/controllers). To do so, pass the controller and action name to the `action` method: -->
[controller actions](/docs/8.x/controllers) へのリダイレクトを生成することもできます。これを行うには、コントローラとアクション名を `action` メソッドに渡します。

```
use App\Http\Controllers\HomeController;

return redirect()->action([HomeController::class, 'index']);
```

<!-- If your controller route requires parameters, you may pass them as the second argument to the `action` method: -->
コントローラ ルートにパラメーターが必要な場合は、それらを `action` メソッドの 2 番目の引数として渡すことができます。

```
return redirect()->action(
    [UserController::class, 'profile'], ['id' => 1]
);
```

<a name="redirecting-with-flashed-session-data"></a>
<!-- ## Redirecting With Flashed Session Data -->
## Redirecting With Flashed Session Data

<!-- Redirecting to a new URL and [flashing data to the session](/docs/8.x/session#flash-data) are usually done at the same time. Typically, this is done after successfully performing an action when you flash a success message to the session. For convenience, you may create a `RedirectResponse` instance and flash data to the session in a single, fluent method chain: -->
通常、新しい URL へのリダイレクトと [flashing data to the session](/docs/8.x/session#flash-data) は同時に行われます。通常、これはアクションが正常に実行された後で、成功メッセージをセッションにフラッシュするときに行われます。便宜上、`RedirectResponse` インスタンスを作成し、単一の滑らかなメソッド チェーンでセッションにデータをフラッシュすることができます。

```
Route::post('/user/profile', function () {
    // Update the user's profile...

    return redirect('/dashboard')->with('status', 'Profile updated!');
});
```

<!-- You may use the `withInput` method provided by the `RedirectResponse` instance to flash the current request's input data to the session before redirecting the user to a new location. Once the input has been flashed to the session, you may easily [retrieve it](/docs/8.x/requests#retrieving-old-input) during the next request: -->
`RedirectResponse` インスタンスによって提供される `withInput` メソッドを使用して、ユーザーを新しい場所にリダイレクトする前に、現在のリクエストの入力データをセッションにフラッシュできます。入力がセッションにフラッシュされると、次のリクエスト中に簡単に [retrieve it](/docs/8.x/requests#retrieving-old-input) を実行できます。

```
return back()->withInput();
```

<!-- After the user is redirected, you may display the flashed message from the [session](/docs/8.x/session). For example, using [Blade syntax](/docs/8.x/blade): -->
ユーザーがリダイレクトされた後、[session](/docs/8.x/session) からフラッシュされたメッセージを表示できます。たとえば、[Blade syntax](/docs/8.x/blade) を使用すると、次のようになります。

```
@if (session('status'))
    <div class="alert alert-success">
        {{ session('status') }}
    </div>
@endif
```

