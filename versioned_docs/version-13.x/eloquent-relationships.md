# Eloquent: 연관관계 (Eloquent: Relationships)

- [소개](#introduction)
- [연관관계 정의하기](#defining-relationships)
    - [일대일 / 하나를 가짐](#one-to-one)
    - [일대다 / 여러 개를 가짐](#one-to-many)
    - [일대다(역방향) / 소속 관계](#one-to-many-inverse)
    - [여러 항목 중 하나를 가짐](#has-one-of-many)
    - [하나를 거쳐 하나를 가짐](#has-one-through)
    - [하나를 거쳐 여러 개를 가짐](#has-many-through)
- [범위가 지정된 연관관계](#scoped-relationships)
- [다대다 연관관계](#many-to-many)
    - [중간 테이블 컬럼 조회하기](#retrieving-intermediate-table-columns)
    - [중간 테이블 컬럼으로 쿼리 필터링하기](#filtering-queries-via-intermediate-table-columns)
    - [중간 테이블 컬럼으로 쿼리 정렬하기](#ordering-queries-via-intermediate-table-columns)
    - [커스텀 중간 테이블 모델 정의하기](#defining-custom-intermediate-table-models)
- [다형성 연관관계](#polymorphic-relationships)
    - [일대일](#one-to-one-polymorphic-relations)
    - [일대다](#one-to-many-polymorphic-relations)
    - [여러 항목 중 하나](#one-of-many-polymorphic-relations)
    - [다대다](#many-to-many-polymorphic-relations)
    - [커스텀 다형성 타입](#custom-polymorphic-types)
- [동적 연관관계](#dynamic-relationships)
- [연관관계 쿼리하기](#querying-relations)
    - [연관관계 메서드와 동적 속성](#relationship-methods-vs-dynamic-properties)
    - [연관관계 존재 여부 쿼리하기](#querying-relationship-existence)
    - [연관관계 부재 여부 쿼리하기](#querying-relationship-absence)
    - [Morph To 연관관계 쿼리하기](#querying-morph-to-relationships)
- [관련 모델 집계하기](#aggregating-related-models)
    - [관련 모델 개수 세기](#counting-related-models)
    - [기타 집계 함수](#other-aggregate-functions)
    - [Morph To 연관관계에서 관련 모델 개수 세기](#counting-related-models-on-morph-to-relationships)
- [Eager Loading](#eager-loading)
    - [Eager Load 제약하기](#constraining-eager-loads)
    - [Lazy Eager Loading](#lazy-eager-loading)
    - [자동 Eager Loading](#automatic-eager-loading)
    - [Lazy Loading 방지하기](#preventing-lazy-loading)
- [관련 모델 삽입 및 업데이트하기](#inserting-and-updating-related-models)
    - [`save` 메서드](#the-save-method)
    - [`create` 메서드](#the-create-method)
    - [Belongs To 연관관계](#updating-belongs-to-relationships)
    - [다대다 연관관계](#updating-many-to-many-relationships)
- [부모 타임스탬프 갱신하기](#touching-parent-timestamps)

<a name="introduction"></a>
## 소개 (Introduction)

데이터베이스 테이블은 서로 관련되어 있는 경우가 많습니다. 예를 들어 블로그 게시물에는 여러 댓글이 있을 수 있고, 주문은 그 주문을 생성한 사용자와 관련될 수 있습니다. Eloquent는 이러한 연관관계를 쉽게 관리하고 다룰 수 있게 해주며, 자주 사용하는 다양한 연관관계를 지원합니다.

<div class="content-list" markdown="1">

- [일대일](#one-to-one)
- [일대다](#one-to-many)
- [다대다](#many-to-many)
- [하나를 거쳐 하나를 가짐](#has-one-through)
- [하나를 거쳐 여러 개를 가짐](#has-many-through)
- [일대일(다형성)](#one-to-one-polymorphic-relations)
- [일대다(다형성)](#one-to-many-polymorphic-relations)
- [다대다(다형성)](#many-to-many-polymorphic-relations)

</div>

<a name="defining-relationships"></a>
## 연관관계 정의하기 (Defining Relationships)

Eloquent 연관관계는 Eloquent 모델 클래스의 메서드로 정의합니다. 연관관계는 강력한 [쿼리 빌더](/docs/13.x/queries) 역할도 하므로, 연관관계를 메서드로 정의하면 강력한 메서드 체이닝과 쿼리 기능을 사용할 수 있습니다. 예를 들어 이 `posts` 연관관계에 추가 쿼리 제약을 이어서 적용할 수 있습니다.

```php
$user->posts()->where('active', 1)->get();
```

하지만 연관관계를 사용하는 방법을 더 깊이 살펴보기 전에, Eloquent가 지원하는 각 연관관계 타입을 정의하는 방법부터 알아보겠습니다.

<a name="one-to-one"></a>
### 일대일 / 하나를 가짐

일대일 연관관계는 매우 기본적인 데이터베이스 연관관계 유형입니다. 예를 들어 `User` 모델은 하나의 `Phone` 모델과 연결될 수 있습니다. 이 연관관계를 정의하려면 `User` 모델에 `phone` 메서드를 추가합니다. `phone` 메서드는 `hasOne` 메서드를 호출하고 그 결과를 반환해야 합니다. `hasOne` 메서드는 모델의 `Illuminate\Database\Eloquent\Model` 기본 클래스를 통해 사용할 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasOne;

class User extends Model
{
    /**
     * Get the phone associated with the user.
     */
    public function phone(): HasOne
    {
        return $this->hasOne(Phone::class);
    }
}
```

`hasOne` 메서드에 전달하는 첫 번째 인수는 관련 모델 클래스의 이름입니다. 연관관계를 정의한 뒤에는 Eloquent의 동적 속성을 사용하여 관련 레코드를 조회할 수 있습니다. 동적 속성을 사용하면 연관관계 메서드를 모델에 정의된 속성처럼 접근할 수 있습니다.

```php
$phone = User::find(1)->phone;
```

Eloquent는 부모 모델 이름을 기준으로 연관관계의 외래 키를 결정합니다. 이 경우 `Phone` 모델에는 `user_id` 외래 키가 있다고 자동으로 가정합니다. 이 규칙을 재정의하고 싶다면 `hasOne` 메서드의 두 번째 인수로 외래 키를 전달할 수 있습니다.

```php
return $this->hasOne(Phone::class, 'foreign_key');
```

또한 Eloquent는 외래 키가 부모 모델의 기본 키 컬럼과 일치하는 값을 가져야 한다고 가정합니다. 다시 말해 Eloquent는 `Phone` 레코드의 `user_id` 컬럼에서 사용자의 `id` 컬럼 값을 찾습니다. 연관관계에서 `id` 또는 모델의 기본 키가 아닌 다른 기본 키 값을 사용하고 싶다면 `hasOne` 메서드의 세 번째 인수로 값을 전달할 수 있습니다.

```php
return $this->hasOne(Phone::class, 'foreign_key', 'local_key');
```

<a name="one-to-one-defining-the-inverse-of-the-relationship"></a>
#### 연관관계의 역방향 정의하기

이제 `User` 모델에서 `Phone` 모델에 접근할 수 있습니다. 다음으로는 전화번호를 소유한 사용자에 접근할 수 있도록 `Phone` 모델에 연관관계를 정의해 보겠습니다. `hasOne` 연관관계의 역방향은 `belongsTo` 메서드를 사용하여 정의할 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Phone extends Model
{
    /**
     * Get the user that owns the phone.
     */
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }
}
```

`user` 메서드를 호출하면 Eloquent는 `Phone` 모델의 `user_id` 컬럼과 일치하는 `id`를 가진 `User` 모델을 찾으려고 시도합니다.

Eloquent는 연관관계 메서드의 이름을 확인한 뒤 메서드 이름에 `_id`를 붙여 외래 키 이름을 결정합니다. 따라서 이 경우 Eloquent는 `Phone` 모델에 `user_id` 컬럼이 있다고 가정합니다. 하지만 `Phone` 모델의 외래 키가 `user_id`가 아니라면 `belongsTo` 메서드의 두 번째 인수로 커스텀 키 이름을 전달할 수 있습니다.

```php
/**
 * Get the user that owns the phone.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class, 'foreign_key');
}
```

부모 모델이 기본 키로 `id`를 사용하지 않거나, 다른 컬럼을 사용해 연결된 모델을 찾고 싶다면 `belongsTo` 메서드의 세 번째 인수로 부모 테이블의 커스텀 키를 지정할 수 있습니다.

```php
/**
 * Get the user that owns the phone.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class, 'foreign_key', 'owner_key');
}
```

<a name="one-to-many"></a>
### 일대다 / 여러 개를 가짐

일대다 연관관계는 하나의 모델이 하나 이상의 자식 모델의 부모가 되는 관계를 정의할 때 사용합니다. 예를 들어 블로그 게시물에는 댓글이 무한히 많이 달릴 수 있습니다. 다른 모든 Eloquent 연관관계와 마찬가지로, 일대다 연관관계도 Eloquent 모델에 메서드를 정의하여 만듭니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Post extends Model
{
    /**
     * Get the comments for the blog post.
     */
    public function comments(): HasMany
    {
        return $this->hasMany(Comment::class);
    }
}
```

Eloquent는 `Comment` 모델에 맞는 외래 키 컬럼을 자동으로 결정한다는 점을 기억하세요. 관례에 따라 Eloquent는 부모 모델 이름을 "snake case"로 바꾸고 뒤에 `_id`를 붙입니다. 따라서 이 예제에서 Eloquent는 `Comment` 모델의 외래 키 컬럼이 `post_id`라고 가정합니다.

연관관계 메서드를 정의한 뒤에는 `comments` 속성에 접근하여 관련 댓글의 [컬렉션](/docs/13.x/eloquent-collections)을 가져올 수 있습니다. Eloquent가 "동적 연관관계 속성"을 제공하므로, 연관관계 메서드를 모델에 정의된 속성처럼 접근할 수 있다는 점을 기억하세요.

```php
use App\Models\Post;

$comments = Post::find(1)->comments;

foreach ($comments as $comment) {
    // ...
}
```

모든 연관관계는 쿼리 빌더 역할도 하므로, `comments` 메서드를 호출한 뒤 쿼리에 조건을 계속 체이닝하여 연관관계 쿼리에 추가 제약을 적용할 수 있습니다.

```php
$comment = Post::find(1)->comments()
    ->where('title', 'foo')
    ->first();
```

`hasOne` 메서드와 마찬가지로, `hasMany` 메서드에 추가 인수를 전달하여 외래 키와 로컬 키를 재정의할 수도 있습니다.

```php
return $this->hasMany(Comment::class, 'foreign_key');

return $this->hasMany(Comment::class, 'foreign_key', 'local_key');
```

<a name="automatically-hydrating-parent-models-on-children"></a>
#### 자식 모델에 부모 모델을 자동으로 하이드레이션하기

Eloquent의 eager loading을 사용하더라도, 자식 모델을 반복 처리하는 중에 자식 모델에서 부모 모델에 접근하려고 하면 "N + 1" 쿼리 문제가 발생할 수 있습니다.

```php
$posts = Post::with('comments')->get();

foreach ($posts as $post) {
    foreach ($post->comments as $comment) {
        echo $comment->post->title;
    }
}
```

위 예제에서는 모든 `Post` 모델에 대해 댓글을 eager loading했지만, Eloquent가 각 자식 `Comment` 모델에 부모 `Post`를 자동으로 하이드레이션하지 않기 때문에 "N + 1" 쿼리 문제가 발생합니다.

Eloquent가 부모 모델을 자식 모델에 자동으로 하이드레이션하도록 하려면 `hasMany` 연관관계를 정의할 때 `chaperone` 메서드를 호출하면 됩니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Post extends Model
{
    /**
     * Get the comments for the blog post.
     */
    public function comments(): HasMany
    {
        return $this->hasMany(Comment::class)->chaperone();
    }
}
```

또는 런타임에 자동 부모 하이드레이션을 선택적으로 적용하고 싶다면, 연관관계를 eager loading할 때 `chaperone` 메서드를 호출할 수 있습니다.

```php
use App\Models\Post;

$posts = Post::with([
    'comments' => fn ($comments) => $comments->chaperone(),
])->get();
```

<a name="one-to-many-inverse"></a>
### 일대다(역방향) / 소속 관계

이제 게시물의 모든 댓글에 접근할 수 있으므로, 댓글이 자신의 부모 게시물에 접근할 수 있도록 연관관계를 정의해 보겠습니다. `hasMany` 연관관계의 역방향을 정의하려면 자식 모델에 `belongsTo` 메서드를 호출하는 연관관계 메서드를 정의합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Comment extends Model
{
    /**
     * Get the post that owns the comment.
     */
    public function post(): BelongsTo
    {
        return $this->belongsTo(Post::class);
    }
}
```

연관관계를 정의한 뒤에는 `post` "동적 연관관계 속성"에 접근하여 댓글의 부모 게시물을 조회할 수 있습니다.

```php
use App\Models\Comment;

$comment = Comment::find(1);

return $comment->post->title;
```

위 예제에서 Eloquent는 `Comment` 모델의 `post_id` 컬럼과 일치하는 `id`를 가진 `Post` 모델을 찾으려고 시도합니다.

Eloquent는 연관관계 메서드의 이름을 확인한 뒤, 메서드 이름에 `_`와 부모 모델의 기본 키 컬럼 이름을 붙여 기본 외래 키 이름을 결정합니다. 따라서 이 예제에서 Eloquent는 `comments` 테이블에 있는 `Post` 모델의 외래 키가 `post_id`라고 가정합니다.

하지만 연관관계의 외래 키가 이러한 관례를 따르지 않는다면 `belongsTo` 메서드의 두 번째 인수로 커스텀 외래 키 이름을 전달할 수 있습니다.

```php
/**
 * Get the post that owns the comment.
 */
public function post(): BelongsTo
{
    return $this->belongsTo(Post::class, 'foreign_key');
}
```

부모 모델이 기본 키로 `id`를 사용하지 않거나, 다른 컬럼을 사용해 연결된 모델을 찾고 싶다면 `belongsTo` 메서드의 세 번째 인수로 부모 테이블의 커스텀 키를 지정할 수 있습니다.

```php
/**
 * Get the post that owns the comment.
 */
public function post(): BelongsTo
{
    return $this->belongsTo(Post::class, 'foreign_key', 'owner_key');
}
```

<a name="default-models"></a>
#### 기본 모델

`belongsTo`, `hasOne`, `hasOneThrough`, `morphOne` 연관관계에서는 주어진 연관관계가 `null`일 때 반환할 기본 모델을 정의할 수 있습니다. 이 패턴은 흔히 [Null Object 패턴](https://en.wikipedia.org/wiki/Null_Object_pattern)이라고 부르며, 코드에서 조건문 검사를 줄이는 데 도움이 됩니다. 다음 예제에서 `Post` 모델에 연결된 사용자가 없으면 `user` 연관관계는 빈 `App\Models\User` 모델을 반환합니다.

```php
/**
 * Get the author of the post.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault();
}
```

기본 모델에 속성을 채우려면 `withDefault` 메서드에 배열이나 클로저를 전달할 수 있습니다.

```php
/**
 * Get the author of the post.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault([
        'name' => 'Guest Author',
    ]);
}

/**
 * Get the author of the post.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault(function (User $user, Post $post) {
        $user->name = 'Guest Author';
    });
}
```

<a name="querying-belongs-to-relationships"></a>
#### Belongs To 연관관계 쿼리하기

"belongs to" 연관관계의 자식 모델을 쿼리할 때는 해당 Eloquent 모델을 조회하기 위해 `where` 절을 직접 작성할 수 있습니다.

```php
use App\Models\Post;

$posts = Post::where('user_id', $user->id)->get();
```

하지만 `whereBelongsTo` 메서드를 사용하면 더 편리할 수 있습니다. 이 메서드는 주어진 모델에 맞는 연관관계와 외래 키를 자동으로 결정합니다.

```php
$posts = Post::whereBelongsTo($user)->get();
```

`whereBelongsTo` 메서드에는 [컬렉션](/docs/13.x/eloquent-collections) 인스턴스를 전달할 수도 있습니다. 이렇게 하면 Laravel은 컬렉션 안의 부모 모델 중 어느 하나에 속하는 모델을 조회합니다.

```php
$users = User::where('vip', true)->get();

$posts = Post::whereBelongsTo($users)->get();
```

기본적으로 Laravel은 주어진 모델의 클래스 이름을 기준으로 해당 모델과 연결된 연관관계를 결정합니다. 하지만 `whereBelongsTo` 메서드의 두 번째 인수로 연관관계 이름을 전달하여 직접 지정할 수도 있습니다.
```php
$posts = Post::whereBelongsTo($user, 'author')->get();
```

<a name="has-one-of-many"></a>
### 다수 중 하나의 Has One 관계

때로는 한 모델에 여러 관련 모델이 있지만, 그 관계에서 "최신" 또는 "가장 오래된" 관련 모델을 쉽게 가져오고 싶을 수 있습니다. 예를 들어 `User` 모델은 여러 `Order` 모델과 관련될 수 있지만, 사용자가 가장 최근에 생성한 주문과 편리하게 상호작용하는 방법을 정의하고 싶을 수 있습니다. `hasOne` 관계 타입과 `ofMany` 메서드를 함께 사용하면 이를 구현할 수 있습니다.

```php
/**
 * Get the user's most recent order.
 */
public function latestOrder(): HasOne
{
    return $this->hasOne(Order::class)->latestOfMany();
}
```

마찬가지로, 관계에서 "가장 오래된" 또는 첫 번째 관련 모델을 가져오는 메서드를 정의할 수도 있습니다.

```php
/**
 * Get the user's oldest order.
 */
public function oldestOrder(): HasOne
{
    return $this->hasOne(Order::class)->oldestOfMany();
}
```

기본적으로 `latestOfMany`와 `oldestOfMany` 메서드는 정렬 가능한 모델의 기본 키를 기준으로 최신 또는 가장 오래된 관련 모델을 가져옵니다. 하지만 더 큰 관계에서 다른 정렬 기준을 사용해 단일 모델을 가져오고 싶을 때도 있습니다.

예를 들어 `ofMany` 메서드를 사용하면 사용자의 가장 비싼 주문을 가져올 수 있습니다. `ofMany` 메서드는 첫 번째 인수로 정렬 가능한 컬럼을 받고, 관련 모델을 조회할 때 적용할 집계 함수(`min` 또는 `max`)를 두 번째 인수로 받습니다.

```php
/**
 * Get the user's largest order.
 */
public function largestOrder(): HasOne
{
    return $this->hasOne(Order::class)->ofMany('price', 'max');
}
```

> [!WARNING]
> PostgreSQL은 UUID 컬럼에 대해 `MAX` 함수를 실행하는 것을 지원하지 않으므로, 현재 PostgreSQL UUID 컬럼과 함께 다수 중 하나 관계를 사용할 수 없습니다.

<a name="converting-many-relationships-to-has-one-relationships"></a>
#### "Many" 관계를 Has One 관계로 변환하기

`latestOfMany`, `oldestOfMany`, 또는 `ofMany` 메서드를 사용해 단일 모델을 가져올 때, 같은 모델에 대해 이미 "has many" 관계가 정의되어 있는 경우가 많습니다. 편의를 위해 Laravel은 관계에서 `one` 메서드를 호출하여 이 관계를 "has one" 관계로 쉽게 변환할 수 있도록 합니다.

```php
/**
 * Get the user's orders.
 */
public function orders(): HasMany
{
    return $this->hasMany(Order::class);
}

/**
 * Get the user's largest order.
 */
public function largestOrder(): HasOne
{
    return $this->orders()->one()->ofMany('price', 'max');
}
```

또한 `one` 메서드를 사용해 `HasManyThrough` 관계를 `HasOneThrough` 관계로 변환할 수도 있습니다.

```php
public function latestDeployment(): HasOneThrough
{
    return $this->deployments()->one()->latestOfMany();
}
```

<a name="advanced-has-one-of-many-relationships"></a>
#### 고급 다수 중 하나의 Has One 관계

더 고급 형태의 "다수 중 하나의 has one" 관계를 구성할 수도 있습니다. 예를 들어 `Product` 모델은 여러 관련 `Price` 모델을 가질 수 있으며, 새로운 가격이 게시된 뒤에도 기존 가격 데이터가 시스템에 보관될 수 있습니다. 또한 제품의 새로운 가격 데이터는 `published_at` 컬럼을 통해 미래 시점부터 적용되도록 미리 게시될 수도 있습니다.

정리하면, 게시일이 미래가 아닌 가격 중에서 가장 최근에 게시된 가격을 가져와야 합니다. 또한 두 가격의 게시일이 같다면 ID가 더 큰 가격을 우선해야 합니다. 이를 구현하려면 최신 가격을 결정하는 정렬 가능한 컬럼이 포함된 배열을 `ofMany` 메서드에 전달해야 합니다. 또한 `ofMany` 메서드의 두 번째 인수로 클로저를 제공합니다. 이 클로저는 관계 쿼리에 추가적인 게시일 제약 조건을 더하는 역할을 합니다.

```php
/**
 * Get the current pricing for the product.
 */
public function currentPricing(): HasOne
{
    return $this->hasOne(Price::class)->ofMany([
        'published_at' => 'max',
        'id' => 'max',
    ], function (Builder $query) {
        $query->where('published_at', '<', now());
    });
}
```

<a name="has-one-through"></a>
### Has One Through 관계

"has-one-through" 관계는 다른 모델과의 일대일 관계를 정의합니다. 다만 이 관계는 선언하는 모델이 세 번째 모델을 _거쳐_ 다른 모델의 한 인스턴스와 연결될 수 있음을 나타냅니다.

예를 들어 차량 수리점 애플리케이션에서 각 `Mechanic` 모델은 하나의 `Car` 모델과 연결될 수 있고, 각 `Car` 모델은 하나의 `Owner` 모델과 연결될 수 있습니다. 정비사와 소유자는 데이터베이스 안에서 직접적인 관계를 갖고 있지 않지만, 정비사는 `Car` 모델을 _통해_ 소유자에 접근할 수 있습니다. 이 관계를 정의하는 데 필요한 테이블을 살펴보겠습니다.

```text
mechanics
    id - integer
    name - string

cars
    id - integer
    model - string
    mechanic_id - integer

owners
    id - integer
    name - string
    car_id - integer
```

이제 관계의 테이블 구조를 살펴보았으니, `Mechanic` 모델에 관계를 정의해 보겠습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasOneThrough;

class Mechanic extends Model
{
    /**
     * Get the car's owner.
     */
    public function carOwner(): HasOneThrough
    {
        return $this->hasOneThrough(Owner::class, Car::class);
    }
}
```

`hasOneThrough` 메서드에 전달되는 첫 번째 인수는 접근하려는 최종 모델의 이름이며, 두 번째 인수는 중간 모델의 이름입니다.

또는 관계에 포함된 모든 모델에 관련 관계가 이미 정의되어 있다면, `through` 메서드를 호출하고 해당 관계 이름을 제공하여 "has-one-through" 관계를 유창하게 정의할 수 있습니다. 예를 들어 `Mechanic` 모델에 `cars` 관계가 있고 `Car` 모델에 `owner` 관계가 있다면, 다음과 같이 정비사와 소유자를 연결하는 "has-one-through" 관계를 정의할 수 있습니다.

```php
// String based syntax...
return $this->through('cars')->has('owner');

// Dynamic syntax...
return $this->throughCars()->hasOwner();
```

<a name="has-one-through-key-conventions"></a>
#### 키 규칙

관계 쿼리를 수행할 때는 일반적인 Eloquent 외래 키 규칙이 사용됩니다. 관계의 키를 직접 지정하고 싶다면 `hasOneThrough` 메서드의 세 번째와 네 번째 인수로 전달할 수 있습니다. 세 번째 인수는 중간 모델에 있는 외래 키의 이름입니다. 네 번째 인수는 최종 모델에 있는 외래 키의 이름입니다. 다섯 번째 인수는 로컬 키이며, 여섯 번째 인수는 중간 모델의 로컬 키입니다.

```php
class Mechanic extends Model
{
    /**
     * Get the car's owner.
     */
    public function carOwner(): HasOneThrough
    {
        return $this->hasOneThrough(
            Owner::class,
            Car::class,
            'mechanic_id', // Foreign key on the cars table...
            'car_id', // Foreign key on the owners table...
            'id', // Local key on the mechanics table...
            'id' // Local key on the cars table...
        );
    }
}
```

또는 앞서 설명한 것처럼, 관계에 포함된 모든 모델에 관련 관계가 이미 정의되어 있다면 `through` 메서드를 호출하고 해당 관계 이름을 제공하여 "has-one-through" 관계를 유창하게 정의할 수 있습니다. 이 접근 방식은 기존 관계에 이미 정의된 키 규칙을 재사용할 수 있다는 장점이 있습니다.

```php
// String based syntax...
return $this->through('cars')->has('owner');

// Dynamic syntax...
return $this->throughCars()->hasOwner();
```

<a name="has-many-through"></a>
### Has Many Through 관계

"has-many-through" 관계는 중간 관계를 통해 멀리 떨어진 관계에 편리하게 접근할 수 있는 방법을 제공합니다. 예를 들어 [Laravel Cloud](https://cloud.laravel.com) 같은 배포 플랫폼을 만들고 있다고 가정해 보겠습니다. `Application` 모델은 중간 `Environment` 모델을 통해 여러 `Deployment` 모델에 접근할 수 있습니다. 이 예시를 사용하면 특정 애플리케이션의 모든 배포를 쉽게 모을 수 있습니다. 이 관계를 정의하는 데 필요한 테이블을 살펴보겠습니다.

```text
applications
    id - integer
    name - string

environments
    id - integer
    application_id - integer
    name - string

deployments
    id - integer
    environment_id - integer
    commit_hash - string
```

이제 관계의 테이블 구조를 살펴보았으니, `Application` 모델에 관계를 정의해 보겠습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasManyThrough;

class Application extends Model
{
    /**
     * Get all of the deployments for the application.
     */
    public function deployments(): HasManyThrough
    {
        return $this->hasManyThrough(Deployment::class, Environment::class);
    }
}
```

`hasManyThrough` 메서드에 전달되는 첫 번째 인수는 접근하려는 최종 모델의 이름이며, 두 번째 인수는 중간 모델의 이름입니다.

또는 관계에 포함된 모든 모델에 관련 관계가 이미 정의되어 있다면, `through` 메서드를 호출하고 해당 관계 이름을 제공하여 "has-many-through" 관계를 유창하게 정의할 수 있습니다. 예를 들어 `Application` 모델에 `environments` 관계가 있고 `Environment` 모델에 `deployments` 관계가 있다면, 다음과 같이 애플리케이션과 배포를 연결하는 "has-many-through" 관계를 정의할 수 있습니다.

```php
// String based syntax...
return $this->through('environments')->has('deployments');

// Dynamic syntax...
return $this->throughEnvironments()->hasDeployments();
```

`Deployment` 모델의 테이블에는 `application_id` 컬럼이 없지만, `hasManyThrough` 관계를 사용하면 `$application->deployments`를 통해 애플리케이션의 배포에 접근할 수 있습니다. 이러한 모델을 가져오기 위해 Eloquent는 중간 `Environment` 모델의 테이블에서 `application_id` 컬럼을 확인합니다. 관련 환경 ID를 찾은 뒤, 그 ID를 사용해 `Deployment` 모델의 테이블을 조회합니다.

<a name="has-many-through-key-conventions"></a>
#### 키 규칙

관계 쿼리를 수행할 때는 일반적인 Eloquent 외래 키 규칙이 사용됩니다. 관계의 키를 직접 지정하고 싶다면 `hasManyThrough` 메서드의 세 번째와 네 번째 인수로 전달할 수 있습니다. 세 번째 인수는 중간 모델에 있는 외래 키의 이름입니다. 네 번째 인수는 최종 모델에 있는 외래 키의 이름입니다. 다섯 번째 인수는 로컬 키이며, 여섯 번째 인수는 중간 모델의 로컬 키입니다.

```php
class Application extends Model
{
    public function deployments(): HasManyThrough
    {
        return $this->hasManyThrough(
            Deployment::class,
            Environment::class,
            'application_id', // Foreign key on the environments table...
            'environment_id', // Foreign key on the deployments table...
            'id', // Local key on the applications table...
            'id' // Local key on the environments table...
        );
    }
}
```

또는 앞서 설명한 것처럼, 관계에 포함된 모든 모델에 관련 관계가 이미 정의되어 있다면 `through` 메서드를 호출하고 해당 관계 이름을 제공하여 "has-many-through" 관계를 유창하게 정의할 수 있습니다. 이 접근 방식은 기존 관계에 이미 정의된 키 규칙을 재사용할 수 있다는 장점이 있습니다.

```php
// String based syntax...
return $this->through('environments')->has('deployments');

// Dynamic syntax...
return $this->throughEnvironments()->hasDeployments();
```

<a name="scoped-relationships"></a>
### 범위가 지정된 관계

관계에 제약을 추가하는 메서드를 모델에 더하는 일은 흔합니다. 예를 들어 `User` 모델에 `featuredPosts` 메서드를 추가해, 더 넓은 `posts` 관계에 추가 `where` 제약을 적용할 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class User extends Model
{
    /**
     * Get the user's posts.
     */
    public function posts(): HasMany
    {
        return $this->hasMany(Post::class)->latest();
    }

    /**
     * Get the user's featured posts.
     */
    public function featuredPosts(): HasMany
    {
        return $this->posts()->where('featured', true);
    }
}
```

하지만 `featuredPosts` 메서드를 통해 모델을 생성하려고 하면 해당 모델의 `featured` 속성은 `true`로 설정되지 않습니다. 관계 메서드를 통해 모델을 생성하면서, 그 관계를 통해 생성되는 모든 모델에 추가되어야 하는 속성도 함께 지정하고 싶다면, 관계 쿼리를 만들 때 `withAttributes` 메서드를 사용할 수 있습니다.

```php
/**
 * Get the user's featured posts.
 */
public function featuredPosts(): HasMany
{
    return $this->posts()->withAttributes(['featured' => true]);
}
```

`withAttributes` 메서드는 주어진 속성을 사용해 쿼리에 `where` 조건을 추가하며, 관계 메서드를 통해 생성되는 모든 모델에도 해당 속성을 추가합니다.

```php
$post = $user->featuredPosts()->create(['title' => 'Featured Post']);

$post->featured; // true
```

`withAttributes` 메서드가 쿼리에 `where` 조건을 추가하지 않도록 하려면 `asConditions` 인수를 `false`로 설정하면 됩니다.

```php
return $this->posts()->withAttributes(['featured' => true], asConditions: false);
```

<a name="many-to-many"></a>
## 다대다 관계 (Many to Many Relationships)

다대다 관계는 `hasOne`과 `hasMany` 관계보다 조금 더 복잡합니다. 다대다 관계의 예로는 여러 역할을 가진 사용자가 있고, 그 역할들이 애플리케이션의 다른 사용자에게도 공유되는 경우가 있습니다. 예를 들어 한 사용자에게 "Author"와 "Editor" 역할을 할당할 수 있습니다. 하지만 그 역할들은 다른 사용자에게도 할당될 수 있습니다. 따라서 사용자는 여러 역할을 가지고, 역할도 여러 사용자를 가집니다.

<a name="many-to-many-table-structure"></a>
#### 테이블 구조

이 관계를 정의하려면 `users`, `roles`, `role_user`라는 세 개의 데이터베이스 테이블이 필요합니다. `role_user` 테이블은 관련 모델 이름을 알파벳 순서로 배열해 만든 이름이며, `user_id`와 `role_id` 컬럼을 포함합니다. 이 테이블은 사용자와 역할을 연결하는 중간 테이블로 사용됩니다.

역할은 여러 사용자에 속할 수 있으므로, 단순히 `roles` 테이블에 `user_id` 컬럼을 둘 수는 없습니다. 그렇게 하면 하나의 역할이 단 한 명의 사용자에게만 속할 수 있다는 뜻이 됩니다. 역할을 여러 사용자에게 할당할 수 있도록 지원하려면 `role_user` 테이블이 필요합니다. 관계의 테이블 구조를 다음과 같이 요약할 수 있습니다.

```text
users
    id - integer
    name - string

roles
    id - integer
    name - string

role_user
    user_id - integer
    role_id - integer
```

<a name="many-to-many-model-structure"></a>
#### 모델 구조

다대다 관계는 `belongsToMany` 메서드의 결과를 반환하는 메서드를 작성하여 정의합니다. `belongsToMany` 메서드는 애플리케이션의 모든 Eloquent 모델이 사용하는 `Illuminate\Database\Eloquent\Model` 기본 클래스에서 제공됩니다. 예를 들어 `User` 모델에 `roles` 메서드를 정의해 보겠습니다. 이 메서드에 전달되는 첫 번째 인수는 관련 모델 클래스의 이름입니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class User extends Model
{
    /**
     * The roles that belong to the user.
     */
    public function roles(): BelongsToMany
    {
        return $this->belongsToMany(Role::class);
    }
}
```

관계를 정의한 뒤에는 `roles` 동적 관계 속성을 사용해 사용자의 역할에 접근할 수 있습니다.

```php
use App\Models\User;

$user = User::find(1);

foreach ($user->roles as $role) {
    // ...
}
```
모든 연관관계는 쿼리 빌더 역할도 하므로, `roles` 메서드를 호출한 뒤 쿼리에 조건을 계속 체이닝하여 연관관계 쿼리에 추가 제약 조건을 더할 수 있습니다:

```php
$roles = User::find(1)->roles()->orderBy('name')->get();
```

연관관계의 중간 테이블 이름을 결정할 때, Eloquent는 관련된 두 모델 이름을 알파벳 순서로 결합합니다. 하지만 이 규칙은 자유롭게 재정의할 수 있습니다. `belongsToMany` 메서드에 두 번째 인수를 전달하면 됩니다:

```php
return $this->belongsToMany(Role::class, 'role_user');
```

중간 테이블 이름을 사용자 지정하는 것뿐만 아니라, `belongsToMany` 메서드에 추가 인수를 전달하여 테이블에 있는 키의 컬럼 이름도 사용자 지정할 수 있습니다. 세 번째 인수는 이 연관관계를 정의하고 있는 모델의 외래 키 이름이고, 네 번째 인수는 조인할 모델의 외래 키 이름입니다:

```php
return $this->belongsToMany(Role::class, 'role_user', 'user_id', 'role_id');
```

<a name="many-to-many-defining-the-inverse-of-the-relationship"></a>
#### 연관관계의 역방향 정의

다대다 연관관계의 "역방향"을 정의하려면, 관련 모델에 `belongsToMany` 메서드의 결과를 반환하는 메서드를 정의해야 합니다. 사용자 / 역할 예제를 완성하기 위해 `Role` 모델에 `users` 메서드를 정의해 보겠습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class Role extends Model
{
    /**
     * The users that belong to the role.
     */
    public function users(): BelongsToMany
    {
        return $this->belongsToMany(User::class);
    }
}
```

보시다시피 `App\Models\User` 모델을 참조한다는 점을 제외하면, 연관관계는 대응되는 `User` 모델의 연관관계와 정확히 같은 방식으로 정의됩니다. `belongsToMany` 메서드를 재사용하므로, 다대다 연관관계의 "역방향"을 정의할 때도 일반적인 테이블 및 키 사용자 지정 옵션을 모두 사용할 수 있습니다.

<a name="retrieving-intermediate-table-columns"></a>
### 중간 테이블 컬럼 조회

이미 살펴본 것처럼 다대다 연관관계를 다루려면 중간 테이블이 필요합니다. Eloquent는 이 테이블과 상호작용할 수 있는 매우 유용한 방법을 제공합니다. 예를 들어 `User` 모델이 여러 `Role` 모델과 관련되어 있다고 가정해 보겠습니다. 이 연관관계에 접근한 뒤에는 모델의 `pivot` 속성을 사용하여 중간 테이블에 접근할 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

foreach ($user->roles as $role) {
    echo $role->pivot->created_at;
}
```

조회된 각 `Role` 모델에 `pivot` 속성이 자동으로 할당된다는 점에 주목하세요. 이 속성은 중간 테이블을 나타내는 모델을 담고 있습니다.

기본적으로 `pivot` 모델에는 모델 키만 포함됩니다. 중간 테이블에 추가 속성이 있다면, 연관관계를 정의할 때 해당 속성을 지정해야 합니다:

```php
return $this->belongsToMany(Role::class)->withPivot('active', 'created_by');
```

중간 테이블에 `created_at` 및 `updated_at` 타임스탬프를 두고 Eloquent가 자동으로 관리하게 하려면, 연관관계를 정의할 때 `withTimestamps` 메서드를 호출하세요:

```php
return $this->belongsToMany(Role::class)->withTimestamps();
```

> [!WARNING]
> Eloquent가 자동으로 관리하는 타임스탬프를 사용하는 중간 테이블에는 `created_at` 및 `updated_at` 타임스탬프 컬럼이 모두 있어야 합니다.

<a name="customizing-the-pivot-attribute-name"></a>
#### `pivot` 속성 이름 사용자 지정

앞서 설명했듯이, 중간 테이블의 속성은 모델에서 `pivot` 속성을 통해 접근할 수 있습니다. 하지만 애플리케이션 안에서의 목적을 더 잘 드러내도록 이 속성의 이름을 자유롭게 사용자 지정할 수 있습니다.

예를 들어 애플리케이션에 팟캐스트를 구독할 수 있는 사용자가 있다면, 사용자와 팟캐스트 사이에는 다대다 연관관계가 있을 가능성이 높습니다. 이런 경우 중간 테이블 속성의 이름을 `pivot` 대신 `subscription`으로 바꾸고 싶을 수 있습니다. 연관관계를 정의할 때 `as` 메서드를 사용하면 됩니다:

```php
return $this->belongsToMany(Podcast::class)
    ->as('subscription')
    ->withTimestamps();
```

사용자 지정 중간 테이블 속성이 지정되면, 사용자 지정한 이름으로 중간 테이블 데이터에 접근할 수 있습니다:

```php
$users = User::with('podcasts')->get();

foreach ($users->flatMap->podcasts as $podcast) {
    echo $podcast->subscription->created_at;
}
```

<a name="filtering-queries-via-intermediate-table-columns"></a>
### 중간 테이블 컬럼을 통한 쿼리 필터링

연관관계를 정의할 때 `wherePivot`, `wherePivotIn`, `wherePivotNotIn`, `wherePivotBetween`, `wherePivotNotBetween`, `wherePivotNull`, `wherePivotNotNull` 메서드를 사용하여 `belongsToMany` 연관관계 쿼리가 반환하는 결과를 필터링할 수도 있습니다:

```php
return $this->belongsToMany(Role::class)
    ->wherePivot('approved', 1);

return $this->belongsToMany(Role::class)
    ->wherePivotIn('priority', [1, 2]);

return $this->belongsToMany(Role::class)
    ->wherePivotNotIn('priority', [1, 2]);

return $this->belongsToMany(Podcast::class)
    ->as('subscriptions')
    ->wherePivotBetween('created_at', ['2020-01-01 00:00:00', '2020-12-31 00:00:00']);

return $this->belongsToMany(Podcast::class)
    ->as('subscriptions')
    ->wherePivotNotBetween('created_at', ['2020-01-01 00:00:00', '2020-12-31 00:00:00']);

return $this->belongsToMany(Podcast::class)
    ->as('subscriptions')
    ->wherePivotNull('expired_at');

return $this->belongsToMany(Podcast::class)
    ->as('subscriptions')
    ->wherePivotNotNull('expired_at');
```

`wherePivot`는 쿼리에 where 절 제약 조건을 추가하지만, 정의된 연관관계를 통해 새 모델을 생성할 때 지정된 값을 추가하지는 않습니다. 특정 pivot 값으로 연관관계를 조회하면서 생성도 해야 한다면 `withPivotValue` 메서드를 사용할 수 있습니다:

```php
return $this->belongsToMany(Role::class)
    ->withPivotValue('approved', 1);
```

<a name="ordering-queries-via-intermediate-table-columns"></a>
### 중간 테이블 컬럼을 통한 쿼리 정렬

`orderByPivot` 및 `orderByPivotDesc` 메서드를 사용하여 `belongsToMany` 연관관계 쿼리가 반환하는 결과를 정렬할 수 있습니다. 다음 예제에서는 사용자의 최신 배지를 모두 조회합니다:

```php
return $this->belongsToMany(Badge::class)
    ->where('rank', 'gold')
    ->orderByPivotDesc('created_at');
```

<a name="defining-custom-intermediate-table-models"></a>
### 사용자 지정 중간 테이블 모델 정의

다대다 연관관계의 중간 테이블을 나타내는 사용자 지정 모델을 정의하고 싶다면, 연관관계를 정의할 때 `using` 메서드를 호출하면 됩니다. 사용자 지정 pivot 모델을 사용하면 메서드나 캐스트처럼 pivot 모델에 추가 동작을 정의할 수 있습니다.

사용자 지정 다대다 pivot 모델은 `Illuminate\Database\Eloquent\Relations\Pivot` 클래스를 확장해야 하며, 사용자 지정 다형성 다대다 pivot 모델은 `Illuminate\Database\Eloquent\Relations\MorphPivot` 클래스를 확장해야 합니다. 예를 들어 사용자 지정 `RoleUser` pivot 모델을 사용하는 `Role` 모델을 정의할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class Role extends Model
{
    /**
     * The users that belong to the role.
     */
    public function users(): BelongsToMany
    {
        return $this->belongsToMany(User::class)->using(RoleUser::class);
    }
}
```

`RoleUser` 모델을 정의할 때는 `Illuminate\Database\Eloquent\Relations\Pivot` 클래스를 확장해야 합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Relations\Pivot;

class RoleUser extends Pivot
{
    // ...
}
```

> [!WARNING]
> Pivot 모델은 `SoftDeletes` trait를 사용할 수 없습니다. pivot 레코드를 소프트 삭제해야 한다면 pivot 모델을 실제 Eloquent 모델로 변환하는 것을 고려하세요.

<a name="custom-pivot-models-and-incrementing-ids"></a>
#### 사용자 지정 Pivot 모델과 증가 ID

사용자 지정 pivot 모델을 사용하는 다대다 연관관계를 정의했고, 그 pivot 모델에 자동 증가 기본 키가 있다면, 사용자 지정 pivot 모델 클래스가 `incrementing`이 `true`로 설정된 `Table` 속성을 사용하도록 해야 합니다:

```php
use Illuminate\Database\Eloquent\Attributes\Table;
use Illuminate\Database\Eloquent\Relations\Pivot;

#[Table(incrementing: true)]
class RoleUser extends Pivot
{
    // ...
}
```

<a name="polymorphic-relationships"></a>
## 다형성 연관관계 (Polymorphic Relationships)

다형성 연관관계를 사용하면 자식 모델이 하나의 연결만으로 여러 타입의 모델에 속할 수 있습니다. 예를 들어 사용자가 블로그 게시글과 동영상을 공유할 수 있는 애플리케이션을 만든다고 가정해 보겠습니다. 이런 애플리케이션에서는 `Comment` 모델이 `Post` 모델과 `Video` 모델 모두에 속할 수 있습니다.

<a name="one-to-one-polymorphic-relations"></a>
### 일대일 (다형성)

<a name="one-to-one-polymorphic-table-structure"></a>
#### 테이블 구조

일대일 다형성 연관관계는 일반적인 일대일 연관관계와 비슷합니다. 하지만 자식 모델이 하나의 연결만으로 여러 타입의 모델에 속할 수 있다는 차이가 있습니다. 예를 들어 블로그 `Post`와 `User`가 `Image` 모델에 대한 다형성 연관관계를 공유할 수 있습니다. 일대일 다형성 연관관계를 사용하면 게시글과 사용자에 연결될 수 있는 고유한 이미지들을 하나의 테이블에 둘 수 있습니다. 먼저 테이블 구조를 살펴보겠습니다:

```text
posts
    id - integer
    name - string

users
    id - integer
    name - string

images
    id - integer
    url - string
    imageable_id - integer
    imageable_type - string
```

`images` 테이블의 `imageable_id` 및 `imageable_type` 컬럼에 주목하세요. `imageable_id` 컬럼에는 게시글 또는 사용자의 ID 값이 들어가며, `imageable_type` 컬럼에는 부모 모델의 클래스 이름이 들어갑니다. `imageable_type` 컬럼은 `imageable` 연관관계에 접근할 때 어떤 "타입"의 부모 모델을 반환해야 하는지 Eloquent가 판단하는 데 사용됩니다. 이 경우 컬럼에는 `App\Models\Post` 또는 `App\Models\User`가 들어갑니다.

<a name="one-to-one-polymorphic-model-structure"></a>
#### 모델 구조

다음으로 이 연관관계를 만들기 위해 필요한 모델 정의를 살펴보겠습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphTo;

class Image extends Model
{
    /**
     * Get the parent imageable model (user or post).
     */
    public function imageable(): MorphTo
    {
        return $this->morphTo();
    }
}

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphOne;

class Post extends Model
{
    /**
     * Get the post's image.
     */
    public function image(): MorphOne
    {
        return $this->morphOne(Image::class, 'imageable');
    }
}

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphOne;

class User extends Model
{
    /**
     * Get the user's image.
     */
    public function image(): MorphOne
    {
        return $this->morphOne(Image::class, 'imageable');
    }
}
```

<a name="one-to-one-polymorphic-retrieving-the-relationship"></a>
#### 연관관계 조회

데이터베이스 테이블과 모델이 정의되면, 모델을 통해 연관관계에 접근할 수 있습니다. 예를 들어 게시글의 이미지를 조회하려면 `image` 동적 연관관계 속성에 접근하면 됩니다:

```php
use App\Models\Post;

$post = Post::find(1);

$image = $post->image;
```

`morphTo` 호출을 수행하는 메서드 이름에 접근하여 다형성 모델의 부모를 조회할 수 있습니다. 이 경우에는 `Image` 모델의 `imageable` 메서드입니다. 따라서 이 메서드에 동적 연관관계 속성처럼 접근합니다:

```php
use App\Models\Image;

$image = Image::find(1);

$imageable = $image->imageable;
```

`Image` 모델의 `imageable` 연관관계는 이미지를 소유한 모델 타입에 따라 `Post` 또는 `User` 인스턴스를 반환합니다.

<a name="morph-one-to-one-key-conventions"></a>
#### 키 규칙

필요하다면 다형성 자식 모델에서 사용하는 "id" 및 "type" 컬럼의 이름을 지정할 수 있습니다. 이렇게 하는 경우, 항상 연관관계 이름을 `morphTo` 메서드의 첫 번째 인수로 전달해야 합니다. 일반적으로 이 값은 메서드 이름과 일치해야 하므로 PHP의 `__FUNCTION__` 상수를 사용할 수 있습니다:

```php
/**
 * Get the model that the image belongs to.
 */
public function imageable(): MorphTo
{
    return $this->morphTo(__FUNCTION__, 'imageable_type', 'imageable_id');
}
```

<a name="one-to-many-polymorphic-relations"></a>
### 일대다 (다형성)

<a name="one-to-many-polymorphic-table-structure"></a>
#### 테이블 구조

일대다 다형성 연관관계는 일반적인 일대다 연관관계와 비슷합니다. 하지만 자식 모델이 하나의 연결만으로 여러 타입의 모델에 속할 수 있다는 차이가 있습니다. 예를 들어 애플리케이션의 사용자가 게시글과 동영상에 "댓글"을 남길 수 있다고 가정해 보겠습니다. 다형성 연관관계를 사용하면 하나의 `comments` 테이블에 게시글과 동영상의 댓글을 모두 담을 수 있습니다. 먼저 이 연관관계를 만들기 위해 필요한 테이블 구조를 살펴보겠습니다:

```text
posts
    id - integer
    title - string
    body - text

videos
    id - integer
    title - string
    url - string

comments
    id - integer
    body - text
    commentable_id - integer
    commentable_type - string
```

<a name="one-to-many-polymorphic-model-structure"></a>
#### 모델 구조

다음으로 이 연관관계를 만들기 위해 필요한 모델 정의를 살펴보겠습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphTo;

class Comment extends Model
{
    /**
     * Get the parent commentable model (post or video).
     */
    public function commentable(): MorphTo
    {
        return $this->morphTo();
    }
}

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphMany;

class Post extends Model
{
    /**
     * Get all of the post's comments.
     */
    public function comments(): MorphMany
    {
        return $this->morphMany(Comment::class, 'commentable');
    }
}

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphMany;

class Video extends Model
{
    /**
     * Get all of the video's comments.
     */
    public function comments(): MorphMany
    {
        return $this->morphMany(Comment::class, 'commentable');
    }
}
```
<a name="one-to-many-polymorphic-retrieving-the-relationship"></a>
#### 연관관계 조회하기

데이터베이스 테이블과 모델을 정의한 후에는 모델의 동적 연관관계 속성을 통해 연관관계에 접근할 수 있습니다. 예를 들어 게시글의 모든 댓글에 접근하려면 `comments` 동적 속성을 사용할 수 있습니다.

```php
use App\Models\Post;

$post = Post::find(1);

foreach ($post->comments as $comment) {
    // ...
}
```

또한 `morphTo` 호출을 수행하는 메서드 이름에 접근하여 다형성 자식 모델의 부모를 조회할 수도 있습니다. 이 경우에는 `Comment` 모델의 `commentable` 메서드입니다. 따라서 댓글의 부모 모델에 접근하기 위해 이 메서드를 동적 연관관계 속성처럼 사용합니다.

```php
use App\Models\Comment;

$comment = Comment::find(1);

$commentable = $comment->commentable;
```

`Comment` 모델의 `commentable` 연관관계는 댓글의 부모가 어떤 모델 타입인지에 따라 `Post` 또는 `Video` 인스턴스를 반환합니다.

<a name="polymorphic-automatically-hydrating-parent-models-on-children"></a>
#### 자식 모델에 부모 모델 자동 하이드레이션하기

Eloquent 즉시 로딩(eager loading)을 사용하더라도, 자식 모델을 반복하면서 자식 모델에서 부모 모델에 접근하려고 하면 "N + 1" 쿼리 문제가 발생할 수 있습니다.

```php
$posts = Post::with('comments')->get();

foreach ($posts as $post) {
    foreach ($post->comments as $comment) {
        echo $comment->commentable->title;
    }
}
```

위 예제에서는 각 `Post` 모델에 대해 댓글을 즉시 로딩했음에도, Eloquent가 각 자식 `Comment` 모델에 부모 `Post`를 자동으로 하이드레이션하지 않기 때문에 "N + 1" 쿼리 문제가 발생합니다.

Eloquent가 부모 모델을 자식 모델에 자동으로 하이드레이션하도록 하려면 `morphMany` 연관관계를 정의할 때 `chaperone` 메서드를 호출하면 됩니다.

```php
class Post extends Model
{
    /**
     * Get all of the post's comments.
     */
    public function comments(): MorphMany
    {
        return $this->morphMany(Comment::class, 'commentable')->chaperone();
    }
}
```

또는 런타임에 연관관계를 즉시 로딩할 때 자동 부모 하이드레이션을 사용하도록 선택하려면 `chaperone` 메서드를 호출하면 됩니다.

```php
use App\Models\Post;

$posts = Post::with([
    'comments' => fn ($comments) => $comments->chaperone(),
])->get();
```

<a name="one-of-many-polymorphic-relations"></a>
### 여러 항목 중 하나 다형성 연관관계

때로는 한 모델이 여러 관련 모델을 가지고 있지만, 그 연관관계에서 "가장 최신" 또는 "가장 오래된" 관련 모델을 쉽게 조회하고 싶을 수 있습니다. 예를 들어 `User` 모델이 여러 `Image` 모델과 연관될 수 있지만, 사용자가 업로드한 가장 최근 이미지를 편리하게 다룰 방법을 정의하고 싶을 수 있습니다. 이는 `morphOne` 연관관계 타입과 `ofMany` 메서드를 함께 사용하여 구현할 수 있습니다.

```php
/**
 * Get the user's most recent image.
 */
public function latestImage(): MorphOne
{
    return $this->morphOne(Image::class, 'imageable')->latestOfMany();
}
```

마찬가지로 연관관계에서 "가장 오래된", 즉 첫 번째 관련 모델을 조회하는 메서드를 정의할 수도 있습니다.

```php
/**
 * Get the user's oldest image.
 */
public function oldestImage(): MorphOne
{
    return $this->morphOne(Image::class, 'imageable')->oldestOfMany();
}
```

기본적으로 `latestOfMany`와 `oldestOfMany` 메서드는 정렬 가능한 모델의 기본 키를 기준으로 가장 최신 또는 가장 오래된 관련 모델을 조회합니다. 하지만 더 큰 연관관계에서 다른 정렬 기준을 사용해 단일 모델을 조회하고 싶을 때도 있습니다.

예를 들어 `ofMany` 메서드를 사용하면 사용자의 가장 많은 "좋아요"를 받은 이미지를 조회할 수 있습니다. `ofMany` 메서드는 첫 번째 인수로 정렬 가능한 컬럼을 받고, 관련 모델을 쿼리할 때 적용할 집계 함수(`min` 또는 `max`)를 받습니다.

```php
/**
 * Get the user's most popular image.
 */
public function bestImage(): MorphOne
{
    return $this->morphOne(Image::class, 'imageable')->ofMany('likes', 'max');
}
```

> [!NOTE]
> 더 고급 "여러 항목 중 하나" 연관관계를 구성할 수도 있습니다. 자세한 내용은 [has one of many 문서](#advanced-has-one-of-many-relationships)를 참고하십시오.

<a name="many-to-many-polymorphic-relations"></a>
### 다대다 다형성 연관관계

<a name="many-to-many-polymorphic-table-structure"></a>
#### 테이블 구조

다대다 다형성 연관관계는 "morph one" 및 "morph many" 연관관계보다 약간 더 복잡합니다. 예를 들어 `Post` 모델과 `Video` 모델이 `Tag` 모델에 대한 다형성 연관관계를 공유할 수 있습니다. 이 상황에서 다대다 다형성 연관관계를 사용하면 애플리케이션은 게시글이나 동영상에 연결될 수 있는 고유한 태그의 단일 테이블을 가질 수 있습니다. 먼저 이 연관관계를 구성하는 데 필요한 테이블 구조를 살펴보겠습니다.

```text
posts
    id - integer
    name - string

videos
    id - integer
    name - string

tags
    id - integer
    name - string

taggables
    tag_id - integer
    taggable_id - integer
    taggable_type - string
```

> [!NOTE]
> 다형성 다대다 연관관계를 살펴보기 전에 일반적인 [다대다 연관관계](#many-to-many)에 대한 문서를 읽어 두면 도움이 됩니다.

<a name="many-to-many-polymorphic-model-structure"></a>
#### 모델 구조

다음으로 모델에 연관관계를 정의할 준비가 되었습니다. `Post`와 `Video` 모델은 모두 기본 Eloquent 모델 클래스가 제공하는 `morphToMany` 메서드를 호출하는 `tags` 메서드를 포함합니다.

`morphToMany` 메서드는 관련 모델의 이름과 "연관관계 이름"을 받습니다. 중간 테이블 이름과 그 테이블이 포함하는 키에 지정한 이름을 기준으로, 이 연관관계를 "taggable"이라고 부르겠습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphToMany;

class Post extends Model
{
    /**
     * Get all of the tags for the post.
     */
    public function tags(): MorphToMany
    {
        return $this->morphToMany(Tag::class, 'taggable');
    }
}
```

<a name="many-to-many-polymorphic-defining-the-inverse-of-the-relationship"></a>
#### 연관관계의 역방향 정의하기

다음으로 `Tag` 모델에는 가능한 각 부모 모델에 대한 메서드를 정의해야 합니다. 따라서 이 예제에서는 `posts` 메서드와 `videos` 메서드를 정의합니다. 이 두 메서드는 모두 `morphedByMany` 메서드의 결과를 반환해야 합니다.

`morphedByMany` 메서드는 관련 모델의 이름과 "연관관계 이름"을 받습니다. 중간 테이블 이름과 그 테이블이 포함하는 키에 지정한 이름을 기준으로, 이 연관관계를 "taggable"이라고 부르겠습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphToMany;

class Tag extends Model
{
    /**
     * Get all of the posts that are assigned this tag.
     */
    public function posts(): MorphToMany
    {
        return $this->morphedByMany(Post::class, 'taggable');
    }

    /**
     * Get all of the videos that are assigned this tag.
     */
    public function videos(): MorphToMany
    {
        return $this->morphedByMany(Video::class, 'taggable');
    }
}
```

<a name="many-to-many-polymorphic-retrieving-the-relationship"></a>
#### 연관관계 조회하기

데이터베이스 테이블과 모델을 정의한 후에는 모델을 통해 연관관계에 접근할 수 있습니다. 예를 들어 게시글의 모든 태그에 접근하려면 `tags` 동적 연관관계 속성을 사용할 수 있습니다.

```php
use App\Models\Post;

$post = Post::find(1);

foreach ($post->tags as $tag) {
    // ...
}
```

다형성 자식 모델에서 `morphedByMany` 호출을 수행하는 메서드 이름에 접근하여 다형성 연관관계의 부모를 조회할 수 있습니다. 이 경우에는 `Tag` 모델의 `posts` 또는 `videos` 메서드입니다.

```php
use App\Models\Tag;

$tag = Tag::find(1);

foreach ($tag->posts as $post) {
    // ...
}

foreach ($tag->videos as $video) {
    // ...
}
```

<a name="custom-polymorphic-types"></a>
### 사용자 정의 다형성 타입

기본적으로 Laravel은 관련 모델의 "타입"을 저장하기 위해 정규화된 클래스 이름을 사용합니다. 예를 들어 위의 일대다 연관관계 예제에서 `Comment` 모델이 `Post` 또는 `Video` 모델에 속할 수 있다면, 기본 `commentable_type`은 각각 `App\Models\Post` 또는 `App\Models\Video`가 됩니다. 하지만 이러한 값을 애플리케이션의 내부 구조와 분리하고 싶을 수 있습니다.

예를 들어 모델 이름을 "타입"으로 사용하는 대신 `post`와 `video` 같은 간단한 문자열을 사용할 수 있습니다. 이렇게 하면 모델 이름이 변경되더라도 데이터베이스의 다형성 "타입" 컬럼 값은 계속 유효하게 유지됩니다.

```php
use Illuminate\Database\Eloquent\Relations\Relation;

Relation::enforceMorphMap([
    'post' => 'App\Models\Post',
    'video' => 'App\Models\Video',
]);
```

`enforceMorphMap` 메서드는 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 호출하거나, 원한다면 별도의 서비스 프로바이더를 만들어 호출할 수 있습니다.

런타임에는 모델의 `getMorphClass` 메서드를 사용하여 특정 모델의 morph alias를 확인할 수 있습니다. 반대로 morph alias와 연결된 정규화된 클래스 이름은 `Relation::getMorphedModel` 메서드를 사용하여 확인할 수 있습니다.

```php
use Illuminate\Database\Eloquent\Relations\Relation;

$alias = $post->getMorphClass();

$class = Relation::getMorphedModel($alias);
```

> [!WARNING]
> 기존 애플리케이션에 "morph map"을 추가할 때, 데이터베이스의 morphable `*_type` 컬럼 값 중 여전히 정규화된 클래스를 포함하는 모든 값은 해당 "map" 이름으로 변환해야 합니다.

<a name="dynamic-relationships"></a>
### 동적 연관관계

`resolveRelationUsing` 메서드를 사용하여 런타임에 Eloquent 모델 간의 연관관계를 정의할 수 있습니다. 일반적인 애플리케이션 개발에서는 보통 권장되지 않지만, Laravel 패키지를 개발할 때 가끔 유용할 수 있습니다.

`resolveRelationUsing` 메서드는 첫 번째 인수로 원하는 연관관계 이름을 받습니다. 이 메서드에 전달되는 두 번째 인수는 모델 인스턴스를 받고 유효한 Eloquent 연관관계 정의를 반환하는 클로저여야 합니다. 일반적으로 동적 연관관계는 [서비스 프로바이더](/docs/13.x/providers)의 boot 메서드 안에서 설정해야 합니다.

```php
use App\Models\Order;
use App\Models\Customer;

Order::resolveRelationUsing('customer', function (Order $orderModel) {
    return $orderModel->belongsTo(Customer::class, 'customer_id');
});
```

> [!WARNING]
> 동적 연관관계를 정의할 때는 항상 Eloquent 연관관계 메서드에 명시적인 키 이름 인수를 제공하십시오.

<a name="querying-relations"></a>
## 연관관계 쿼리하기 (Querying Relations)

모든 Eloquent 연관관계는 메서드를 통해 정의되므로, 실제로 관련 모델을 로드하는 쿼리를 실행하지 않고도 해당 메서드를 호출하여 연관관계 인스턴스를 얻을 수 있습니다. 또한 모든 종류의 Eloquent 연관관계는 [쿼리 빌더](/docs/13.x/queries)로도 동작하므로, 최종적으로 데이터베이스에 대해 SQL 쿼리를 실행하기 전에 연관관계 쿼리에 계속 제약 조건을 체이닝할 수 있습니다.

예를 들어 `User` 모델이 여러 관련 `Post` 모델을 가지는 블로그 애플리케이션을 생각해 보겠습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class User extends Model
{
    /**
     * Get all of the posts for the user.
     */
    public function posts(): HasMany
    {
        return $this->hasMany(Post::class);
    }
}
```

다음과 같이 `posts` 연관관계를 쿼리하고 연관관계에 추가 제약 조건을 더할 수 있습니다.

```php
use App\Models\User;

$user = User::find(1);

$user->posts()->where('active', 1)->get();
```

연관관계에서는 Laravel [쿼리 빌더](/docs/13.x/queries)의 모든 메서드를 사용할 수 있으므로, 사용할 수 있는 모든 메서드를 알아보려면 쿼리 빌더 문서를 살펴보십시오.

<a name="chaining-orwhere-clauses-after-relationships"></a>
#### 연관관계 뒤에 `orWhere` 절 연결하기

위 예제에서 보았듯이 연관관계를 쿼리할 때 추가 제약 조건을 자유롭게 더할 수 있습니다. 하지만 연관관계에 `orWhere` 절을 체이닝할 때는 주의해야 합니다. `orWhere` 절은 연관관계 제약 조건과 같은 수준에서 논리적으로 그룹화되기 때문입니다.

```php
$user->posts()
    ->where('active', 1)
    ->orWhere('votes', '>=', 100)
    ->get();
```

위 예제는 다음 SQL을 생성합니다. 보시다시피 `or` 절은 100표 이상을 받은 _모든_ 게시글을 반환하도록 쿼리에 지시합니다. 이 쿼리는 더 이상 특정 사용자로 제한되지 않습니다.

```sql
select *
from posts
where user_id = ? and active = 1 or votes >= 100
```

대부분의 상황에서는 조건 검사를 괄호로 묶기 위해 [논리 그룹](/docs/13.x/queries#logical-grouping)을 사용해야 합니다.

```php
use Illuminate\Database\Eloquent\Builder;

$user->posts()
    ->where(function (Builder $query) {
        return $query->where('active', 1)
            ->orWhere('votes', '>=', 100);
    })
    ->get();
```

위 예제는 다음 SQL을 생성합니다. 논리 그룹화가 제약 조건을 올바르게 묶었으며, 쿼리가 여전히 특정 사용자로 제한된다는 점에 주목하십시오.

```sql
select *
from posts
where user_id = ? and (active = 1 or votes >= 100)
```

<a name="relationship-methods-vs-dynamic-properties"></a>
### 연관관계 메서드와 동적 속성

Eloquent 연관관계 쿼리에 추가 제약 조건을 더할 필요가 없다면, 연관관계를 속성처럼 접근할 수 있습니다. 예를 들어 앞서 사용한 `User`와 `Post` 예제 모델을 계속 사용하면, 다음과 같이 사용자의 모든 게시글에 접근할 수 있습니다.

```php
use App\Models\User;

$user = User::find(1);

foreach ($user->posts as $post) {
    // ...
}
```

동적 연관관계 속성은 "지연 로딩(lazy loading)"을 수행합니다. 즉, 실제로 속성에 접근할 때에만 연관관계 데이터를 로드합니다. 이 때문에 개발자들은 모델을 로드한 후 접근할 것이라고 알고 있는 연관관계를 미리 로드하기 위해 [즉시 로딩](#eager-loading)을 자주 사용합니다. 즉시 로딩은 모델의 연관관계를 로드하기 위해 실행해야 하는 SQL 쿼리 수를 크게 줄여 줍니다.

<a name="querying-relationship-existence"></a>
### 연관관계 존재 여부 쿼리하기

모델 레코드를 조회할 때 연관관계의 존재 여부를 기준으로 결과를 제한하고 싶을 수 있습니다. 예를 들어 댓글이 하나 이상 있는 모든 블로그 게시글을 조회하고 싶다고 가정해 보겠습니다. 이렇게 하려면 연관관계 이름을 `has` 및 `orHas` 메서드에 전달하면 됩니다.

```php
use App\Models\Post;

// Retrieve all posts that have at least one comment...
$posts = Post::has('comments')->get();
```

쿼리를 더 세밀하게 조정하기 위해 연산자와 개수 값을 지정할 수도 있습니다.

```php
// Retrieve all posts that have three or more comments...
$posts = Post::has('comments', '>=', 3)->get();
```
중첩된 `has` 문은 "점" 표기법을 사용하여 구성할 수 있습니다. 예를 들어, 이미지가 하나 이상 있는 댓글을 하나 이상 가진 모든 게시물을 조회할 수 있습니다.

```php
// Retrieve posts that have at least one comment with images...
$posts = Post::has('comments.images')->get();
```

더 강력한 기능이 필요하다면 `whereHas` 및 `orWhereHas` 메서드를 사용하여 `has` 쿼리에 추가 쿼리 제약을 정의할 수 있습니다. 예를 들어 댓글의 내용을 검사할 수 있습니다.

```php
use Illuminate\Database\Eloquent\Builder;

// Retrieve posts with at least one comment containing words like code%...
$posts = Post::whereHas('comments', function (Builder $query) {
    $query->where('content', 'like', 'code%');
})->get();

// Retrieve posts with at least ten comments containing words like code%...
$posts = Post::whereHas('comments', function (Builder $query) {
    $query->where('content', 'like', 'code%');
}, '>=', 10)->get();
```

> [!WARNING]
> Eloquent는 현재 데이터베이스를跨いだ 연관관계 존재 쿼리를 지원하지 않습니다. 연관관계는 반드시 같은 데이터베이스 안에 있어야 합니다.

<a name="many-to-many-relationship-existence-queries"></a>
#### 다대다 연관관계 존재 쿼리

`whereAttachedTo` 메서드는 특정 모델 또는 모델 컬렉션과 다대다로 연결된 모델을 쿼리할 때 사용할 수 있습니다.

```php
$users = User::whereAttachedTo($role)->get();
```

`whereAttachedTo` 메서드에 [컬렉션](/docs/13.x/eloquent-collections) 인스턴스를 전달할 수도 있습니다. 이렇게 하면 Laravel은 컬렉션 안의 모델 중 하나라도 연결되어 있는 모델을 조회합니다.

```php
$tags = Tag::whereLike('name', '%laravel%')->get();

$posts = Post::whereAttachedTo($tags)->get();
```

<a name="inline-relationship-existence-queries"></a>
#### 인라인 연관관계 존재 쿼리

연관관계 쿼리에 단순한 where 조건 하나만 붙여 연관관계의 존재 여부를 쿼리하고 싶다면 `whereRelation`, `orWhereRelation`, `whereMorphRelation`, `orWhereMorphRelation` 메서드를 사용하는 것이 더 편리할 수 있습니다. 예를 들어 승인되지 않은 댓글이 있는 모든 게시물을 쿼리할 수 있습니다.

```php
use App\Models\Post;

$posts = Post::whereRelation('comments', 'is_approved', false)->get();
```

물론 쿼리 빌더의 `where` 메서드를 호출할 때처럼 연산자를 지정할 수도 있습니다.

```php
$posts = Post::whereRelation(
    'comments', 'created_at', '>=', now()->minus(hours: 1)
)->get();
```

<a name="querying-relationship-absence"></a>
### 연관관계 부재 쿼리하기

모델 레코드를 조회할 때 연관관계가 없는 경우를 기준으로 결과를 제한하고 싶을 수 있습니다. 예를 들어 댓글이 하나도 **없는** 모든 블로그 게시물을 조회한다고 가정해 보겠습니다. 이를 위해 연관관계의 이름을 `doesntHave` 및 `orDoesntHave` 메서드에 전달할 수 있습니다.

```php
use App\Models\Post;

$posts = Post::doesntHave('comments')->get();
```

더 강력한 기능이 필요하다면 `whereDoesntHave` 및 `orWhereDoesntHave` 메서드를 사용하여 `doesntHave` 쿼리에 추가 쿼리 제약을 더할 수 있습니다. 예를 들어 댓글의 내용을 검사할 수 있습니다.

```php
use Illuminate\Database\Eloquent\Builder;

$posts = Post::whereDoesntHave('comments', function (Builder $query) {
    $query->where('content', 'like', 'code%');
})->get();
```

"점" 표기법을 사용하여 중첩된 연관관계에 대해 쿼리를 실행할 수 있습니다. 예를 들어 다음 쿼리는 댓글이 없는 모든 게시물과, 댓글은 있지만 그 댓글 중 어느 것도 차단된 사용자가 작성하지 않은 게시물을 조회합니다.

```php
use Illuminate\Database\Eloquent\Builder;

$posts = Post::whereDoesntHave('comments.author', function (Builder $query) {
    $query->where('banned', 1);
})->get();
```

<a name="querying-morph-to-relationships"></a>
### Morph To 연관관계 쿼리하기

"morph to" 연관관계의 존재 여부를 쿼리하려면 `whereHasMorph` 및 `whereDoesntHaveMorph` 메서드를 사용할 수 있습니다. 이 메서드들은 첫 번째 인수로 연관관계의 이름을 받습니다. 그다음 쿼리에 포함하려는 관련 모델의 이름을 받습니다. 마지막으로 연관관계 쿼리를 커스터마이징하는 클로저를 제공할 수 있습니다.

```php
use App\Models\Comment;
use App\Models\Post;
use App\Models\Video;
use Illuminate\Database\Eloquent\Builder;

// Retrieve comments associated to posts or videos with a title like code%...
$comments = Comment::whereHasMorph(
    'commentable',
    [Post::class, Video::class],
    function (Builder $query) {
        $query->where('title', 'like', 'code%');
    }
)->get();

// Retrieve comments associated to posts with a title not like code%...
$comments = Comment::whereDoesntHaveMorph(
    'commentable',
    Post::class,
    function (Builder $query) {
        $query->where('title', 'like', 'code%');
    }
)->get();
```

때로는 관련 다형성 모델의 "type"에 따라 쿼리 제약을 추가해야 할 수 있습니다. `whereHasMorph` 메서드에 전달되는 클로저는 두 번째 인수로 `$type` 값을 받을 수 있습니다. 이 인수를 사용하면 현재 만들어지고 있는 쿼리의 "type"을 검사할 수 있습니다.

```php
use Illuminate\Database\Eloquent\Builder;

$comments = Comment::whereHasMorph(
    'commentable',
    [Post::class, Video::class],
    function (Builder $query, string $type) {
        $column = $type === Post::class ? 'content' : 'title';

        $query->where($column, 'like', 'code%');
    }
)->get();
```

때로는 "morph to" 연관관계의 부모에 속한 자식 모델을 쿼리하고 싶을 수 있습니다. 이 작업은 `whereMorphedTo` 및 `whereNotMorphedTo` 메서드를 사용하여 수행할 수 있으며, 이 메서드들은 주어진 모델에 맞는 적절한 morph type 매핑을 자동으로 결정합니다. 이 메서드들은 첫 번째 인수로 `morphTo` 연관관계의 이름을 받고, 두 번째 인수로 관련 부모 모델을 받습니다.

```php
$comments = Comment::whereMorphedTo('commentable', $post)
    ->orWhereMorphedTo('commentable', $video)
    ->get();
```

<a name="querying-all-morph-to-related-models"></a>
#### 모든 관련 모델 쿼리하기

가능한 다형성 모델의 배열을 전달하는 대신, 와일드카드 값으로 `*`를 제공할 수 있습니다. 이렇게 하면 Laravel은 데이터베이스에서 가능한 모든 다형성 타입을 조회합니다. Laravel은 이 작업을 수행하기 위해 추가 쿼리를 실행합니다.

```php
use Illuminate\Database\Eloquent\Builder;

$comments = Comment::whereHasMorph('commentable', '*', function (Builder $query) {
    $query->where('title', 'like', 'foo%');
})->get();
```

<a name="aggregating-related-models"></a>
## 관련 모델 집계 (Aggregating Related Models)

<a name="counting-related-models"></a>
### 관련 모델 개수 세기

때로는 실제로 모델을 로드하지 않고도 특정 연관관계에 연결된 관련 모델의 개수를 세고 싶을 수 있습니다. 이를 위해 `withCount` 메서드를 사용할 수 있습니다. `withCount` 메서드는 결과 모델에 `{relation}_count` 속성을 추가합니다.

```php
use App\Models\Post;

$posts = Post::withCount('comments')->get();

foreach ($posts as $post) {
    echo $post->comments_count;
}
```

`withCount` 메서드에 배열을 전달하면 여러 연관관계의 "개수"를 추가할 수 있으며, 쿼리에 추가 제약도 더할 수 있습니다.

```php
use Illuminate\Database\Eloquent\Builder;

$posts = Post::withCount(['votes', 'comments' => function (Builder $query) {
    $query->where('content', 'like', 'code%');
}])->get();

echo $posts[0]->votes_count;
echo $posts[0]->comments_count;
```

연관관계 개수 결과에 별칭을 지정할 수도 있으므로, 같은 연관관계에 대해 여러 개수를 가져올 수 있습니다.

```php
use Illuminate\Database\Eloquent\Builder;

$posts = Post::withCount([
    'comments',
    'comments as pending_comments_count' => function (Builder $query) {
        $query->where('approved', false);
    },
])->get();

echo $posts[0]->comments_count;
echo $posts[0]->pending_comments_count;
```

<a name="deferred-count-loading"></a>
#### 지연 개수 로딩

`loadCount` 메서드를 사용하면 부모 모델을 이미 조회한 뒤에 연관관계 개수를 로드할 수 있습니다.

```php
$book = Book::first();

$book->loadCount('genres');
```

개수 쿼리에 추가 쿼리 제약을 설정해야 한다면, 개수를 세려는 연관관계를 키로 가지는 배열을 전달할 수 있습니다. 배열의 값은 쿼리 빌더 인스턴스를 받는 클로저여야 합니다.

```php
$book->loadCount(['reviews' => function (Builder $query) {
    $query->where('rating', 5);
}])
```

<a name="relationship-counting-and-custom-select-statements"></a>
#### 연관관계 개수 세기와 커스텀 Select 문

`withCount`를 `select` 문과 함께 사용하는 경우, 반드시 `select` 메서드 뒤에 `withCount`를 호출해야 합니다.

```php
$posts = Post::select(['title', 'body'])
    ->withCount('comments')
    ->get();
```

<a name="other-aggregate-functions"></a>
### 다른 집계 함수

`withCount` 메서드 외에도 Eloquent는 `withMin`, `withMax`, `withAvg`, `withSum`, `withExists` 메서드를 제공합니다. 이 메서드들은 결과 모델에 `{relation}_{function}_{column}` 속성을 추가합니다.

```php
use App\Models\Post;

$posts = Post::withSum('comments', 'votes')->get();

foreach ($posts as $post) {
    echo $post->comments_sum_votes;
}
```

집계 함수의 결과를 다른 이름으로 접근하고 싶다면 직접 별칭을 지정할 수 있습니다.

```php
$posts = Post::withSum('comments as total_comments', 'votes')->get();

foreach ($posts as $post) {
    echo $post->total_comments;
}
```

`loadCount` 메서드와 마찬가지로, 이 메서드들의 지연 로딩 버전도 사용할 수 있습니다. 이미 조회한 Eloquent 모델에 대해 이러한 추가 집계 작업을 수행할 수 있습니다.

```php
$post = Post::first();

$post->loadSum('comments', 'votes');
```

이러한 집계 메서드를 `select` 문과 함께 사용하는 경우, 반드시 `select` 메서드 뒤에 집계 메서드를 호출해야 합니다.

```php
$posts = Post::select(['title', 'body'])
    ->withExists('comments')
    ->get();
```

<a name="counting-related-models-on-morph-to-relationships"></a>
### Morph To 연관관계에서 관련 모델 개수 세기

"morph to" 연관관계를 즉시 로딩하면서, 해당 연관관계가 반환할 수 있는 다양한 엔티티의 관련 모델 개수도 함께 로드하고 싶다면 `with` 메서드와 `morphTo` 연관관계의 `morphWithCount` 메서드를 함께 사용할 수 있습니다.

이 예제에서는 `Photo` 및 `Post` 모델이 `ActivityFeed` 모델을 생성할 수 있다고 가정하겠습니다. `ActivityFeed` 모델은 `parentable`이라는 "morph to" 연관관계를 정의하며, 이를 통해 특정 `ActivityFeed` 인스턴스의 부모 `Photo` 또는 `Post` 모델을 조회할 수 있다고 가정합니다. 또한 `Photo` 모델은 `Tag` 모델을 "have many" 하고, `Post` 모델은 `Comment` 모델을 "have many" 한다고 가정하겠습니다.

이제 `ActivityFeed` 인스턴스를 조회하면서 각 `ActivityFeed` 인스턴스의 `parentable` 부모 모델을 즉시 로딩하고 싶다고 가정해 보겠습니다. 추가로 각 부모 사진에 연결된 태그 수와 각 부모 게시물에 연결된 댓글 수를 조회하고 싶습니다.

```php
use Illuminate\Database\Eloquent\Relations\MorphTo;

$activities = ActivityFeed::with([
    'parentable' => function (MorphTo $morphTo) {
        $morphTo->morphWithCount([
            Photo::class => ['tags'],
            Post::class => ['comments'],
        ]);
    }])->get();
```

<a name="morph-to-deferred-count-loading"></a>
#### 지연 개수 로딩

이미 `ActivityFeed` 모델 집합을 조회했고, 이제 활동 피드와 연결된 여러 `parentable` 모델의 중첩 연관관계 개수를 로드하고 싶다고 가정하겠습니다. 이를 위해 `loadMorphCount` 메서드를 사용할 수 있습니다.

```php
$activities = ActivityFeed::with('parentable')->get();

$activities->loadMorphCount('parentable', [
    Photo::class => ['tags'],
    Post::class => ['comments'],
]);
```

<a name="eager-loading"></a>
## 즉시 로딩 (Eager Loading)

Eloquent 연관관계를 속성처럼 접근하면 관련 모델은 "지연 로딩"됩니다. 이는 해당 속성에 처음 접근하기 전까지 연관관계 데이터가 실제로 로드되지 않는다는 뜻입니다. 하지만 Eloquent는 부모 모델을 쿼리하는 시점에 연관관계를 "즉시 로딩"할 수 있습니다. 즉시 로딩은 "N + 1" 쿼리 문제를 완화합니다. N + 1 쿼리 문제를 설명하기 위해 `Author` 모델에 "belongs to" 하는 `Book` 모델을 살펴보겠습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Book extends Model
{
    /**
     * Get the author that wrote the book.
     */
    public function author(): BelongsTo
    {
        return $this->belongsTo(Author::class);
    }
}
```

이제 모든 책과 그 저자를 조회해 보겠습니다.

```php
use App\Models\Book;

$books = Book::all();

foreach ($books as $book) {
    echo $book->author->name;
}
```

이 반복문은 데이터베이스 테이블 안의 모든 책을 조회하기 위해 쿼리 하나를 실행한 다음, 각 책의 저자를 조회하기 위해 책마다 추가 쿼리를 실행합니다. 따라서 책이 25권 있다면 위 코드는 총 26개의 쿼리를 실행합니다. 책을 조회하는 원래 쿼리 1개와 각 책의 저자를 조회하는 추가 쿼리 25개입니다.

다행히 즉시 로딩을 사용하면 이 작업을 단 두 개의 쿼리로 줄일 수 있습니다. 쿼리를 만들 때 `with` 메서드를 사용하여 즉시 로딩할 연관관계를 지정할 수 있습니다.

```php
$books = Book::with('author')->get();

foreach ($books as $book) {
    echo $book->author->name;
}
```

이 작업에서는 모든 책을 조회하는 쿼리 하나와 모든 책의 모든 저자를 조회하는 쿼리 하나, 총 두 개의 쿼리만 실행됩니다.

```sql
select * from books

select * from authors where id in (1, 2, 3, 4, 5, ...)
```

<a name="eager-loading-multiple-relationships"></a>
#### 여러 연관관계 즉시 로딩

때로는 여러 개의 서로 다른 연관관계를 즉시 로딩해야 할 수 있습니다. 이를 위해 `with` 메서드에 연관관계 배열을 전달하면 됩니다.

```php
$books = Book::with(['author', 'publisher'])->get();
```

<a name="nested-eager-loading"></a>
#### 중첩 즉시 로딩

어떤 연관관계의 또 다른 연관관계를 즉시 로딩하려면 "점" 문법을 사용할 수 있습니다. 예를 들어 모든 책의 저자와 모든 저자의 개인 연락처를 즉시 로딩해 보겠습니다.

```php
$books = Book::with('author.contacts')->get();
```

또는 `with` 메서드에 중첩 배열을 제공하여 중첩 즉시 로딩 연관관계를 지정할 수도 있습니다. 여러 중첩 연관관계를 즉시 로딩할 때 이 방식이 편리할 수 있습니다.

```php
$books = Book::with([
    'author' => [
        'contacts',
        'publisher',
    ],
])->get();
```

<a name="nested-eager-loading-morphto-relationships"></a>
#### 중첩된 `morphTo` 연관관계 즉시 로딩
`morphTo` 연관관계와 함께, 해당 연관관계가 반환할 수 있는 여러 엔티티의 중첩된 연관관계도 즉시 로드하려면 `with` 메서드와 `morphTo` 연관관계의 `morphWith` 메서드를 함께 사용할 수 있습니다. 이 메서드를 설명하기 위해 다음 모델을 살펴보겠습니다.

```php
<?php

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphTo;

class ActivityFeed extends Model
{
    /**
     * Get the parent of the activity feed record.
     */
    public function parentable(): MorphTo
    {
        return $this->morphTo();
    }
}
```

이 예제에서는 `Event`, `Photo`, `Post` 모델이 `ActivityFeed` 모델을 생성할 수 있다고 가정하겠습니다. 또한 `Event` 모델은 `Calendar` 모델에 속하고, `Photo` 모델은 `Tag` 모델과 연결되어 있으며, `Post` 모델은 `Author` 모델에 속한다고 가정하겠습니다.

이러한 모델 정의와 연관관계를 사용하면 `ActivityFeed` 모델 인스턴스를 조회하면서 모든 `parentable` 모델과 각각의 중첩된 연관관계를 즉시 로드할 수 있습니다.

```php
use Illuminate\Database\Eloquent\Relations\MorphTo;

$activities = ActivityFeed::query()
    ->with(['parentable' => function (MorphTo $morphTo) {
        $morphTo->morphWith([
            Event::class => ['calendar'],
            Photo::class => ['tags'],
            Post::class => ['author'],
        ]);
    }])->get();
```

<a name="eager-loading-specific-columns"></a>
#### 특정 컬럼 즉시 로드

조회하는 연관관계의 모든 컬럼이 항상 필요한 것은 아닙니다. 이런 경우를 위해 Eloquent는 연관관계에서 조회할 컬럼을 지정할 수 있도록 합니다.

```php
$books = Book::with('author:id,name,book_id')->get();
```

> [!WARNING]
> 이 기능을 사용할 때는 조회하려는 컬럼 목록에 항상 `id` 컬럼과 관련된 외래 키 컬럼을 포함해야 합니다.

<a name="eager-loading-by-default"></a>
#### 기본으로 즉시 로드

모델을 조회할 때마다 특정 연관관계를 항상 로드하고 싶을 때가 있습니다. 이를 위해 모델에 `$with` 속성을 정의할 수 있습니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Book extends Model
{
    /**
     * The relationships that should always be loaded.
     *
     * @var array
     */
    protected $with = ['author'];

    /**
     * Get the author that wrote the book.
     */
    public function author(): BelongsTo
    {
        return $this->belongsTo(Author::class);
    }

    /**
     * Get the genre of the book.
     */
    public function genre(): BelongsTo
    {
        return $this->belongsTo(Genre::class);
    }
}
```

단일 쿼리에서 `$with` 속성에 포함된 항목을 제거하고 싶다면 `without` 메서드를 사용할 수 있습니다.

```php
$books = Book::without('author')->get();
```

단일 쿼리에서 `$with` 속성 안의 모든 항목을 재정의하고 싶다면 `withOnly` 메서드를 사용할 수 있습니다.

```php
$books = Book::withOnly('genre')->get();
```

<a name="constraining-eager-loads"></a>
### 즉시 로드 제약 조건 지정

연관관계를 즉시 로드하면서, 즉시 로드 쿼리에 추가 쿼리 조건을 지정하고 싶을 때가 있습니다. 이를 위해 `with` 메서드에 연관관계 배열을 전달할 수 있습니다. 배열의 키는 연관관계 이름이고, 값은 즉시 로드 쿼리에 추가 제약 조건을 더하는 클로저입니다.

```php
use App\Models\User;

$users = User::with(['posts' => function ($query) {
    $query->where('title', 'like', '%code%');
}])->get();
```

이 예제에서 Eloquent는 `title` 컬럼에 `code`라는 단어가 포함된 게시물만 즉시 로드합니다. 다른 [쿼리 빌더](/docs/13.x/queries) 메서드를 호출하여 즉시 로드 작업을 더 세부적으로 조정할 수도 있습니다.

```php
$users = User::with(['posts' => function ($query) {
    $query->orderBy('created_at', 'desc');
}])->get();
```

<a name="constraining-eager-loading-of-morph-to-relationships"></a>
#### `morphTo` 연관관계의 즉시 로드 제약 조건 지정

`morphTo` 연관관계를 즉시 로드하면 Eloquent는 관련 모델의 각 타입을 가져오기 위해 여러 쿼리를 실행합니다. `MorphTo` 관계의 `constrain` 메서드를 사용하면 각 쿼리에 추가 제약 조건을 지정할 수 있습니다.

```php
use Illuminate\Database\Eloquent\Relations\MorphTo;

$comments = Comment::with(['commentable' => function (MorphTo $morphTo) {
    $morphTo->constrain([
        Post::class => function ($query) {
            $query->whereNull('hidden_at');
        },
        Video::class => function ($query) {
            $query->where('type', 'educational');
        },
    ]);
}])->get();
```

이 예제에서 Eloquent는 숨겨지지 않은 게시물과 `type` 값이 "educational"인 비디오만 즉시 로드합니다.

<a name="constraining-eager-loads-with-relationship-existence"></a>
#### 연관관계 존재 조건과 함께 즉시 로드 제약 조건 지정

때로는 같은 조건을 기준으로 연관관계의 존재 여부를 확인하면서 동시에 해당 연관관계를 로드해야 할 수 있습니다. 예를 들어, 주어진 쿼리 조건과 일치하는 자식 `Post` 모델을 가진 `User` 모델만 조회하면서, 일치하는 게시물도 함께 즉시 로드하고 싶을 수 있습니다. 이 작업은 `withWhereHas` 메서드를 사용하여 수행할 수 있습니다.

```php
use App\Models\User;

$users = User::withWhereHas('posts', function ($query) {
    $query->where('featured', true);
})->get();
```

<a name="lazy-eager-loading"></a>
### 지연 즉시 로드

부모 모델을 이미 조회한 뒤에 연관관계를 즉시 로드해야 할 때가 있습니다. 예를 들어, 관련 모델을 로드할지 여부를 동적으로 결정해야 하는 경우 유용할 수 있습니다.

```php
use App\Models\Book;

$books = Book::all();

if ($condition) {
    $books->load('author', 'publisher');
}
```

즉시 로드 쿼리에 추가 쿼리 제약 조건을 설정해야 한다면, 로드하려는 연관관계를 키로 하는 배열을 전달할 수 있습니다. 배열의 값은 쿼리 인스턴스를 받는 클로저 인스턴스여야 합니다.

```php
$author->load(['books' => function ($query) {
    $query->orderBy('published_date', 'asc');
}]);
```

연관관계가 아직 로드되지 않았을 때만 로드하려면 `loadMissing` 메서드를 사용합니다.

```php
$book->loadMissing('author');
```

<a name="nested-lazy-eager-loading-morphto"></a>
#### 중첩 지연 즉시 로드와 `morphTo`

`morphTo` 연관관계와 함께, 해당 연관관계가 반환할 수 있는 여러 엔티티의 중첩된 연관관계도 즉시 로드하려면 `loadMorph` 메서드를 사용할 수 있습니다.

이 메서드는 첫 번째 인수로 `morphTo` 연관관계의 이름을 받고, 두 번째 인수로 모델 / 연관관계 쌍의 배열을 받습니다. 이 메서드를 설명하기 위해 다음 모델을 살펴보겠습니다.

```php
<?php

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphTo;

class ActivityFeed extends Model
{
    /**
     * Get the parent of the activity feed record.
     */
    public function parentable(): MorphTo
    {
        return $this->morphTo();
    }
}
```

이 예제에서는 `Event`, `Photo`, `Post` 모델이 `ActivityFeed` 모델을 생성할 수 있다고 가정하겠습니다. 또한 `Event` 모델은 `Calendar` 모델에 속하고, `Photo` 모델은 `Tag` 모델과 연결되어 있으며, `Post` 모델은 `Author` 모델에 속한다고 가정하겠습니다.

이러한 모델 정의와 연관관계를 사용하면 `ActivityFeed` 모델 인스턴스를 조회하면서 모든 `parentable` 모델과 각각의 중첩된 연관관계를 즉시 로드할 수 있습니다.

```php
$activities = ActivityFeed::with('parentable')
    ->get()
    ->loadMorph('parentable', [
        Event::class => ['calendar'],
        Photo::class => ['tags'],
        Post::class => ['author'],
    ]);
```

<a name="automatic-eager-loading"></a>
### 자동 즉시 로드

> [!WARNING]
> 이 기능은 현재 커뮤니티 피드백을 수집하기 위해 베타 상태입니다. 이 기능의 동작과 기능은 패치 릴리스에서도 변경될 수 있습니다.

많은 경우 Laravel은 사용자가 접근하는 연관관계를 자동으로 즉시 로드할 수 있습니다. 자동 즉시 로드를 활성화하려면 애플리케이션의 `AppServiceProvider`에 있는 `boot` 메서드 안에서 `Model::automaticallyEagerLoadRelationships` 메서드를 호출해야 합니다.

```php
use Illuminate\Database\Eloquent\Model;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Model::automaticallyEagerLoadRelationships();
}
```

이 기능이 활성화되면 Laravel은 이전에 로드되지 않은 연관관계에 접근할 때 해당 연관관계를 자동으로 로드하려고 시도합니다. 예를 들어 다음 상황을 살펴보겠습니다.

```php
use App\Models\User;

$users = User::all();

foreach ($users as $user) {
    foreach ($user->posts as $post) {
        foreach ($post->comments as $comment) {
            echo $comment->content;
        }
    }
}
```

일반적으로 위 코드는 각 사용자의 게시물을 조회하기 위해 사용자마다 쿼리를 실행하고, 각 게시물의 댓글을 조회하기 위해 게시물마다 쿼리를 실행합니다. 하지만 `automaticallyEagerLoadRelationships` 기능이 활성화되어 있으면, 조회된 사용자 중 하나의 게시물에 접근하는 순간 Laravel은 사용자 컬렉션의 모든 사용자에 대한 게시물을 자동으로 [지연 즉시 로드](#lazy-eager-loading)합니다. 마찬가지로 조회된 게시물 중 하나의 댓글에 접근하면, 원래 조회된 모든 게시물에 대한 모든 댓글이 지연 즉시 로드됩니다.

자동 즉시 로드를 전역으로 활성화하고 싶지 않다면, 컬렉션에서 `withRelationshipAutoloading` 메서드를 호출하여 단일 Eloquent 컬렉션 인스턴스에 대해서만 이 기능을 활성화할 수도 있습니다.

```php
$users = User::where('vip', true)->get();

return $users->withRelationshipAutoloading();
```

<a name="preventing-lazy-loading"></a>
### 지연 로딩 방지

앞서 설명했듯이, 연관관계를 즉시 로드하면 애플리케이션 성능에 큰 이점을 제공하는 경우가 많습니다. 따라서 원한다면 Laravel이 연관관계의 지연 로딩을 항상 방지하도록 지시할 수 있습니다. 이를 위해 기본 Eloquent 모델 클래스가 제공하는 `preventLazyLoading` 메서드를 호출할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 `AppServiceProvider` 클래스에 있는 `boot` 메서드 안에서 호출해야 합니다.

`preventLazyLoading` 메서드는 지연 로딩을 방지할지 여부를 나타내는 선택적 불리언 인수를 받습니다. 예를 들어, 운영 환경에서는 실수로 지연 로드되는 연관관계가 프로덕션 코드에 있더라도 애플리케이션이 정상적으로 계속 동작하도록 하고, 비운영 환경에서만 지연 로딩을 비활성화하고 싶을 수 있습니다.

```php
use Illuminate\Database\Eloquent\Model;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Model::preventLazyLoading(! $this->app->isProduction());
}
```

지연 로딩을 방지한 뒤에는 애플리케이션이 Eloquent 연관관계를 지연 로드하려고 시도할 때 Eloquent가 `Illuminate\Database\LazyLoadingViolationException` 예외를 발생시킵니다.

`handleLazyLoadingViolationsUsing` 메서드를 사용하여 지연 로딩 위반 동작을 사용자 정의할 수 있습니다. 예를 들어 이 메서드를 사용하면 지연 로딩 위반이 예외로 애플리케이션 실행을 중단하지 않고 로그에만 기록되도록 지시할 수 있습니다.

```php
Model::handleLazyLoadingViolationUsing(function (Model $model, string $relation) {
    $class = $model::class;

    info("Attempted to lazy load [{$relation}] on model [{$class}].");
});
```

<a name="inserting-and-updating-related-models"></a>
## 연관 모델 삽입 및 업데이트 (Inserting and Updating Related Models)

<a name="the-save-method"></a>
### `save` 메서드

Eloquent는 연관관계에 새 모델을 추가하기 위한 편리한 메서드를 제공합니다. 예를 들어 게시물에 새 댓글을 추가해야 한다고 가정해 보겠습니다. `Comment` 모델의 `post_id` 속성을 수동으로 설정하는 대신, 연관관계의 `save` 메서드를 사용하여 댓글을 삽입할 수 있습니다.

```php
use App\Models\Comment;
use App\Models\Post;

$comment = new Comment(['message' => 'A new comment.']);

$post = Post::find(1);

$post->comments()->save($comment);
```

여기서 `comments` 연관관계를 동적 속성으로 접근하지 않았다는 점에 주의하세요. 대신 `comments` 메서드를 호출하여 연관관계 인스턴스를 얻었습니다. `save` 메서드는 새 `Comment` 모델에 적절한 `post_id` 값을 자동으로 추가합니다.

여러 관련 모델을 저장해야 한다면 `saveMany` 메서드를 사용할 수 있습니다.

```php
$post = Post::find(1);

$post->comments()->saveMany([
    new Comment(['message' => 'A new comment.']),
    new Comment(['message' => 'Another new comment.']),
]);
```

`save`와 `saveMany` 메서드는 전달된 모델 인스턴스를 영구 저장하지만, 새로 저장된 모델을 부모 모델에 이미 로드되어 있는 인메모리 연관관계에는 추가하지 않습니다. `save` 또는 `saveMany` 메서드를 사용한 뒤 연관관계에 접근할 계획이라면, `refresh` 메서드를 사용하여 모델과 연관관계를 다시 로드하는 것이 좋습니다.

```php
$post->comments()->save($comment);

$post->refresh();

// All comments, including the newly saved comment...
$post->comments;
```

<a name="the-push-method"></a>
#### 모델과 연관관계 재귀적으로 저장

모델과 그에 연결된 모든 연관관계를 `save`하고 싶다면 `push` 메서드를 사용할 수 있습니다. 이 예제에서는 `Post` 모델뿐 아니라 댓글과 댓글의 작성자도 함께 저장됩니다.

```php
$post = Post::find(1);

$post->comments[0]->message = 'Message';
$post->comments[0]->author->name = 'Author Name';

$post->push();
```

`pushQuietly` 메서드는 이벤트를 발생시키지 않고 모델과 연결된 연관관계를 저장할 때 사용할 수 있습니다.

```php
$post->pushQuietly();
```

<a name="the-create-method"></a>
### `create` 메서드

`save`와 `saveMany` 메서드 외에도 `create` 메서드를 사용할 수 있습니다. 이 메서드는 속성 배열을 받아 모델을 생성하고 데이터베이스에 삽입합니다. `save`와 `create`의 차이는 `save`는 완전한 Eloquent 모델 인스턴스를 받는 반면, `create`는 일반 PHP `array`를 받는다는 점입니다. 새로 생성된 모델은 `create` 메서드에서 반환됩니다.

```php
use App\Models\Post;

$post = Post::find(1);

$comment = $post->comments()->create([
    'message' => 'A new comment.',
]);
```

여러 관련 모델을 생성하려면 `createMany` 메서드를 사용할 수 있습니다.

```php
$post = Post::find(1);

$post->comments()->createMany([
    ['message' => 'A new comment.'],
    ['message' => 'Another new comment.'],
]);
```

`createQuietly`와 `createManyQuietly` 메서드는 이벤트를 디스패치하지 않고 모델을 생성할 때 사용할 수 있습니다.

```php
$user = User::find(1);

$user->posts()->createQuietly([
    'title' => 'Post title.',
]);

$user->posts()->createManyQuietly([
    ['title' => 'First post.'],
    ['title' => 'Second post.'],
]);
```
`findOrNew`, `firstOrNew`, `firstOrCreate`, `updateOrCreate` 메서드를 사용하여 [연관관계에서 모델을 생성하고 업데이트](/docs/13.x/eloquent#upserts)할 수도 있습니다.

> [!NOTE]
> `create` 메서드를 사용하기 전에 반드시 [대량 할당](/docs/13.x/eloquent#mass-assignment) 문서를 검토하세요.

<a name="updating-belongs-to-relationships"></a>
### Belongs To 연관관계

자식 모델을 새 부모 모델에 할당하려면 `associate` 메서드를 사용할 수 있습니다. 이 예제에서 `User` 모델은 `Account` 모델에 대한 `belongsTo` 연관관계를 정의합니다. 이 `associate` 메서드는 자식 모델의 외래 키를 설정합니다.

```php
use App\Models\Account;

$account = Account::find(10);

$user->account()->associate($account);

$user->save();
```

자식 모델에서 부모 모델을 제거하려면 `dissociate` 메서드를 사용할 수 있습니다. 이 메서드는 연관관계의 외래 키를 `null`로 설정합니다.

```php
$user->account()->dissociate();

$user->save();
```

<a name="updating-many-to-many-relationships"></a>
### 다대다 연관관계

<a name="attaching-detaching"></a>
#### 연결 / 분리

Eloquent는 다대다 연관관계를 더 편리하게 다룰 수 있는 메서드도 제공합니다. 예를 들어, 한 사용자가 여러 역할을 가질 수 있고 한 역할도 여러 사용자를 가질 수 있다고 생각해 보겠습니다. `attach` 메서드를 사용하면 연관관계의 중간 테이블에 레코드를 삽입하여 사용자에게 역할을 연결할 수 있습니다.

```php
use App\Models\User;

$user = User::find(1);

$user->roles()->attach($roleId);
```

모델에 연관관계를 연결할 때, 중간 테이블에 함께 삽입할 추가 데이터 배열을 전달할 수도 있습니다.

```php
$user->roles()->attach($roleId, ['expires' => $expires]);
```

때로는 사용자에게서 역할을 제거해야 할 수 있습니다. 다대다 연관관계 레코드를 제거하려면 `detach` 메서드를 사용합니다. `detach` 메서드는 중간 테이블에서 해당 레코드를 삭제하지만, 두 모델은 모두 데이터베이스에 그대로 남아 있습니다.

```php
// Detach a single role from the user...
$user->roles()->detach($roleId);

// Detach all roles from the user...
$user->roles()->detach();
```

편의를 위해 `attach`와 `detach`는 ID 배열도 입력으로 받을 수 있습니다.

```php
$user = User::find(1);

$user->roles()->detach([1, 2, 3]);

$user->roles()->attach([
    1 => ['expires' => $expires],
    2 => ['expires' => $expires],
]);
```

<a name="syncing-associations"></a>
#### 연관 연결 동기화

`sync` 메서드를 사용하여 다대다 연결을 구성할 수도 있습니다. `sync` 메서드는 중간 테이블에 배치할 ID 배열을 받습니다. 주어진 배열에 없는 ID는 중간 테이블에서 제거됩니다. 따라서 이 작업이 완료되면, 중간 테이블에는 주어진 배열에 있는 ID만 존재하게 됩니다.

```php
$user->roles()->sync([1, 2, 3]);
```

ID와 함께 추가 중간 테이블 값을 전달할 수도 있습니다.

```php
$user->roles()->sync([1 => ['expires' => true], 2, 3]);
```

동기화되는 각 모델 ID에 동일한 중간 테이블 값을 삽입하려면 `syncWithPivotValues` 메서드를 사용할 수 있습니다.

```php
$user->roles()->syncWithPivotValues([1, 2, 3], ['active' => true]);
```

주어진 배열에 없는 기존 ID를 분리하고 싶지 않다면 `syncWithoutDetaching` 메서드를 사용할 수 있습니다.

```php
$user->roles()->syncWithoutDetaching([1, 2, 3]);
```

<a name="toggling-associations"></a>
#### 연관 연결 토글

다대다 연관관계는 주어진 관련 모델 ID의 연결 상태를 "토글"하는 `toggle` 메서드도 제공합니다. 주어진 ID가 현재 연결되어 있으면 분리됩니다. 마찬가지로 현재 분리되어 있으면 연결됩니다.

```php
$user->roles()->toggle([1, 2, 3]);
```

ID와 함께 추가 중간 테이블 값을 전달할 수도 있습니다.

```php
$user->roles()->toggle([
    1 => ['expires' => true],
    2 => ['expires' => true],
]);
```

<a name="transactional-pivot-operations"></a>
#### 트랜잭션 기반 Pivot 작업

위에서 설명한 각 Pivot 작업에는 `OrFail` 변형(`attachOrFail`, `detachOrFail`, `syncOrFail`, `syncWithoutDetachingOrFail`, `toggleOrFail`)도 있습니다. 이 변형들은 작업을 데이터베이스 트랜잭션 안에서 실행하므로, 예외가 발생하면 모든 변경 사항이 자동으로 롤백됩니다.

```php
$user->roles()->attachOrFail([1, 2, 3]);

$user->roles()->syncOrFail([1, 2, 3]);
```

<a name="updating-a-record-on-the-intermediate-table"></a>
#### 중간 테이블의 레코드 업데이트

연관관계의 중간 테이블에 있는 기존 행을 업데이트해야 한다면 `updateExistingPivot` 메서드를 사용할 수 있습니다. 이 메서드는 중간 레코드의 외래 키와 업데이트할 속성 배열을 받습니다.

```php
$user = User::find(1);

$user->roles()->updateExistingPivot($roleId, [
    'active' => false,
]);
```

<a name="touching-parent-timestamps"></a>
## 부모 타임스탬프 갱신 (Touching Parent Timestamps)

모델이 다른 모델에 대한 `belongsTo` 또는 `belongsToMany` 연관관계를 정의하는 경우가 있습니다. 예를 들어 `Comment`가 `Post`에 속하는 상황처럼 말입니다. 이런 경우 자식 모델이 업데이트될 때 부모 모델의 타임스탬프도 함께 업데이트하면 유용할 때가 있습니다.

예를 들어 `Comment` 모델이 업데이트될 때, 소유자인 `Post`의 `updated_at` 타임스탬프를 자동으로 "touch"하여 현재 날짜와 시간으로 설정하고 싶을 수 있습니다. 이를 위해 자식 모델에 `Touches` 속성을 사용할 수 있습니다. 이 속성에는 자식 모델이 업데이트될 때 `updated_at` 타임스탬프도 함께 업데이트되어야 하는 연관관계 이름을 지정합니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Touches;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

#[Touches(['post'])]
class Comment extends Model
{
    /**
     * Get the post that the comment belongs to.
     */
    public function post(): BelongsTo
    {
        return $this->belongsTo(Post::class);
    }
}
```

> [!WARNING]
> 부모 모델의 타임스탬프는 자식 모델이 Eloquent의 `save` 메서드를 사용해 업데이트된 경우에만 업데이트됩니다.
