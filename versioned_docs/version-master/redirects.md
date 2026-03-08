# HTTP 리다이렉트 (HTTP Redirects)

- [리다이렉트 생성하기](#creating-redirects)
- [이름이 지정된 라우트로 리다이렉트하기](#redirecting-named-routes)
- [컨트롤러 액션으로 리다이렉트하기](#redirecting-controller-actions)
- [플래시 세션 데이터와 함께 리다이렉트하기](#redirecting-with-flashed-session-data)

<a name="creating-redirects"></a>
## 리다이렉트 생성하기 (Creating Redirects)

리다이렉트 응답은 `Illuminate\Http\RedirectResponse` 클래스의 인스턴스이며, 사용자를 다른 URL로 리다이렉트하는 데 필요한 적절한 헤더를 포함합니다. `RedirectResponse` 인스턴스를 생성하는 방법은 여러 가지가 있지만, 가장 간단한 방법은 전역 헬퍼 함수 `redirect`를 사용하는 것입니다:

```php
Route::get('/dashboard', function () {
    return redirect('/home/dashboard');
});
```

가끔은 사용자를 이전 위치로 리다이렉트하고 싶을 때가 있습니다. 예를 들어, 제출된 폼이 유효하지 않을 경우입니다. 이때는 전역 `back` 헬퍼 함수를 사용할 수 있습니다. 이 기능은 [세션](/docs/master/session)을 사용하므로, `back` 함수를 호출하는 라우트가 반드시 `web` 미들웨어 그룹을 사용하거나 모든 세션 관련 미들웨어가 적용되어 있어야 합니다:

```php
Route::post('/user/profile', function () {
    // 요청을 검증합니다...

    return back()->withInput();
});
```

<a name="redirecting-named-routes"></a>
## 이름이 지정된 라우트로 리다이렉트하기 (Redirecting To Named Routes)

`redirect` 헬퍼를 인수 없이 호출하면, `Illuminate\Routing\Redirector` 인스턴스가 반환되어 `Redirector` 인스턴스의 메서드를 호출할 수 있습니다. 예를 들어, 이름이 지정된 라우트로 리다이렉트 응답을 생성하고 싶다면 `route` 메서드를 사용할 수 있습니다:

```php
return redirect()->route('login');
```

라우트에 파라미터가 필요할 경우, `route` 메서드의 두 번째 인수로 배열 형태로 파라미터를 전달할 수 있습니다:

```php
// URI가 profile/{id}인 라우트 예시

return redirect()->route('profile', ['id' => 1]);
```

편의를 위해 Laravel은 전역 `to_route` 함수도 제공합니다:

```php
return to_route('profile', ['id' => 1]);
```

<a name="populating-parameters-via-eloquent-models"></a>
#### Eloquent 모델로 파라미터 자동 채우기

"ID" 파라미터가 Eloquent 모델에서 채워지는 라우트로 리다이렉트할 경우, 모델 자체를 전달할 수 있습니다. 그러면 ID가 자동으로 추출됩니다:

```php
// URI가 profile/{id}인 라우트 예시

return redirect()->route('profile', [$user]);
```

만약 라우트 파라미터에 들어갈 값을 커스터마이징하려면, Eloquent 모델의 `getRouteKey` 메서드를 오버라이드하면 됩니다:

```php
/**
 * 모델의 라우트 키 값을 반환합니다.
 */
public function getRouteKey(): mixed
{
    return $this->slug;
}
```

<a name="redirecting-controller-actions"></a>
## 컨트롤러 액션으로 리다이렉트하기 (Redirecting To Controller Actions)

컨트롤러 액션으로도 리다이렉트를 생성할 수 있습니다. 이를 위해 `action` 메서드에 컨트롤러와 액션 이름을 전달하면 됩니다:

```php
use App\Http\Controllers\HomeController;

return redirect()->action([HomeController::class, 'index']);
```

컨트롤러 라우트가 파라미터를 필요로 한다면, `action` 메서드의 두 번째 인수로 파라미터를 전달할 수 있습니다:

```php
return redirect()->action(
    [UserController::class, 'profile'], ['id' => 1]
);
```

<a name="redirecting-with-flashed-session-data"></a>
## 플래시 세션 데이터와 함께 리다이렉트하기 (Redirecting With Flashed Session Data)

새 URL로 리다이렉트하면서 동시에 [세션에 데이터를 플래시](https://laravel.com/docs/master/session#flash-data)하는 작업은 보통 한 번에 이뤄집니다. 보통 작업이 성공적으로 완료된 후 성공 메시지를 세션에 플래시할 때 사용됩니다. 편의를 위해 `RedirectResponse` 인스턴스를 생성하면서 데이터를 세션에 플래시하는 메서드 체이닝도 가능합니다:

```php
Route::post('/user/profile', function () {
    // 사용자의 프로필을 업데이트합니다...

    return redirect('/dashboard')->with('status', 'Profile updated!');
});
```

`RedirectResponse` 인스턴스가 제공하는 `withInput` 메서드를 사용하면, 현재 요청의 입력 데이터를 세션에 플래시한 뒤 사용자를 새 위치로 리다이렉트할 수 있습니다. 입력 데이터가 세션에 플래시된 후에는 다음 요청에서 쉽게 [이전 입력값을 조회할 수 있습니다](/docs/master/requests#retrieving-old-input):

```php
return back()->withInput();
```

리다이렉트 후, 세션의 플래시 메시지를 [세션](/docs/master/session)에서 불러와 화면에 표시할 수 있습니다. 예를 들어, [Blade 문법](/docs/master/blade)을 사용할 경우 다음과 같습니다:

```blade
@if (session('status'))
    <div class="alert alert-success">
        {{ session('status') }}
    </div>
@endif
```