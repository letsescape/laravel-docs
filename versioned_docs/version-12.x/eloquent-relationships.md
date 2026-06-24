<!-- # Eloquent: Relationships -->
# Eloquent: Relationships

- [Introduction](#introduction)
- [Defining Relationships](#defining-relationships)
    - [One to One / Has One](#one-to-one)
    - [One to Many / Has Many](#one-to-many)
    - [One to Many (Inverse) / Belongs To](#one-to-many-inverse)
    - [Has One of Many](#has-one-of-many)
    - [Has One Through](#has-one-through)
    - [Has Many Through](#has-many-through)
- [Scoped Relationships](#scoped-relationships)
- [Many to Many Relationships](#many-to-many)
    - [Retrieving Intermediate Table Columns](#retrieving-intermediate-table-columns)
    - [Filtering Queries via Intermediate Table Columns](#filtering-queries-via-intermediate-table-columns)
    - [Ordering Queries via Intermediate Table Columns](#ordering-queries-via-intermediate-table-columns)
    - [Defining Custom Intermediate Table Models](#defining-custom-intermediate-table-models)
- [Polymorphic Relationships](#polymorphic-relationships)
    - [One to One](#one-to-one-polymorphic-relations)
    - [One to Many](#one-to-many-polymorphic-relations)
    - [One of Many](#one-of-many-polymorphic-relations)
    - [Many to Many](#many-to-many-polymorphic-relations)
    - [Custom Polymorphic Types](#custom-polymorphic-types)
- [Dynamic Relationships](#dynamic-relationships)
- [Querying Relations](#querying-relations)
    - [Relationship Methods vs. Dynamic Properties](#relationship-methods-vs-dynamic-properties)
    - [Querying Relationship Existence](#querying-relationship-existence)
    - [Querying Relationship Absence](#querying-relationship-absence)
    - [Querying Morph To Relationships](#querying-morph-to-relationships)
- [Aggregating Related Models](#aggregating-related-models)
    - [Counting Related Models](#counting-related-models)
    - [Other Aggregate Functions](#other-aggregate-functions)
    - [Counting Related Models on Morph To Relationships](#counting-related-models-on-morph-to-relationships)
- [Eager Loading](#eager-loading)
    - [Constraining Eager Loads](#constraining-eager-loads)
    - [Lazy Eager Loading](#lazy-eager-loading)
    - [Automatic Eager Loading](#automatic-eager-loading)
    - [Preventing Lazy Loading](#preventing-lazy-loading)
- [Inserting and Updating Related Models](#inserting-and-updating-related-models)
    - [The `save` Method](#the-save-method)
    - [The `create` Method](#the-create-method)
    - [Belongs To Relationships](#updating-belongs-to-relationships)
    - [Many to Many Relationships](#updating-many-to-many-relationships)
- [Touching Parent Timestamps](#touching-parent-timestamps)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Database tables are often related to one another. For example, a blog post may have many comments or an order could be related to the user who placed it. Eloquent makes managing and working with these relationships easy, and supports a variety of common relationships: -->
데이터베이스 테이블은 종종 서로 연관되어 있습니다. 예를 들어, 블로그 게시글은 여러 개의 댓글을 가질 수 있고, 주문은 주문한 사용자와 연관되어 있을 수 있습니다. Eloquent는 이러한 연관관계를 쉽게 관리하고 작업할 수 있게 해주며, 다음과 같은 일반적인 연관관계를 지원합니다:

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

- [One To One](#one-to-one)
- [One To Many](#one-to-many)
- [Many To Many](#many-to-many)
- [Has One Through](#has-one-through)
- [Has Many Through](#has-many-through)
- [One To One (Polymorphic)](#one-to-one-polymorphic-relations)
- [One To Many (Polymorphic)](#one-to-many-polymorphic-relations)
- [Many To Many (Polymorphic)](#many-to-many-polymorphic-relations)

<!-- </div> -->
</div>

<a name="defining-relationships"></a>
<!-- ## Defining Relationships -->
## Defining Relationships

<!-- Eloquent relationships are defined as methods on your Eloquent model classes. Since relationships also serve as powerful [query builders](/docs/12.x/queries), defining relationships as methods provides powerful method chaining and querying capabilities. For example, we may chain additional query constraints on this `posts` relationship: -->
Eloquent 연관관계는 각각의 Eloquent 모델 클래스의 메서드로 정의합니다. 연관관계는 강력한 [query builders](/docs/12.x/queries)이기도 하므로, 메서드로 정의하면 체이닝과 다양한 쿼리 제약 조건을 쉽게 사용할 수 있습니다. 예를 들어, 아래처럼 `posts` 연관관계에 추가 제약 조건을 붙일 수 있습니다:

```php
$user->posts()->where('active', 1)->get();
```

<!-- But, before diving too deep into using relationships, let's learn how to define each type of relationship supported by Eloquent. -->
연관관계 사용법을 더 깊이 살펴보기 전에, Eloquent에서 지원하는 각 연관관계 정의 방법을 알아봅니다.

<a name="one-to-one"></a>
<!-- ### One to One / Has One -->
### One to One / Has One

<!-- A one-to-one relationship is a very basic type of database relationship. For example, a `User` model might be associated with one `Phone` model. To define this relationship, we will place a `phone` method on the `User` model. The `phone` method should call the `hasOne` method and return its result. The `hasOne` method is available to your model via the model's `Illuminate\Database\Eloquent\Model` base class: -->
일대일 연관관계는 가장 기본적인 데이터베이스 연관관계입니다. 예를 들어, `User` 모델은 하나의 `Phone` 모델과만 연관될 수 있습니다. 이를 정의하려면, `User` 모델에 `phone` 메서드를 추가하고, 해당 `phone` 메서드에서 `hasOne` 메서드를 호출해 반환하면 됩니다. `hasOne` 메서드는 모델의 `Illuminate\Database\Eloquent\Model` 기본 클래스에서 제공됩니다:

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

<!-- The first argument passed to the `hasOne` method is the name of the related model class. Once the relationship is defined, we may retrieve the related record using Eloquent's dynamic properties. Dynamic properties allow you to access relationship methods as if they were properties defined on the model: -->
`hasOne` 메서드의 첫 번째 인수는 연관된 모델 클래스명입니다. 연관관계가 정의되면, Eloquent의 동적 속성을 통해 연관된 레코드를 조회할 수 있습니다. 동적 속성은 연관관계 메서드를 마치 모델의 속성처럼 호출할 수 있게 해줍니다:

```php
$phone = User::find(1)->phone;
```

<!-- Eloquent determines the foreign key of the relationship based on the parent model name. In this case, the `Phone` model is automatically assumed to have a `user_id` foreign key. If you wish to override this convention, you may pass a second argument to the `hasOne` method: -->
Eloquent는 부모 모델 이름을 바탕으로 외래키(foreign key) 컬럼명을 자동으로 결정합니다. 위 예제에서는 `Phone` 모델이 `user_id`라는 외래키를 가진 것으로 간주합니다. 이 규칙을 변경하려면 `hasOne`의 두 번째 인수로 직접 외래키를 지정할 수 있습니다:

```php
return $this->hasOne(Phone::class, 'foreign_key');
```

<!-- Additionally, Eloquent assumes that the foreign key should have a value matching the primary key column of the parent. In other words, Eloquent will look for the value of the user's `id` column in the `user_id` column of the `Phone` record. If you would like the relationship to use a primary key value other than `id` or your model's `$primaryKey` property, you may pass a third argument to the `hasOne` method: -->
또한, Eloquent는 외래키의 값이 부모 모델의 기본키(primary key) 컬럼값과 같아야 한다고 가정합니다. 즉, `Phone` 레코드의 `user_id` 컬럼에서 사용자의 `id` 컬럼값과 일치하는 값을 찾습니다. 만약 `id`나 모델의 `$primaryKey`가 아닌 다른 컬럼을 사용할 경우, `hasOne`의 세 번째 인수로 로컬 키를 지정할 수 있습니다:

```php
return $this->hasOne(Phone::class, 'foreign_key', 'local_key');
```

<a name="one-to-one-defining-the-inverse-of-the-relationship"></a>
<!-- #### Defining the Inverse of the Relationship -->
#### Defining the Inverse of the Relationship

<!-- So, we can access the `Phone` model from our `User` model. Next, let's define a relationship on the `Phone` model that will let us access the user that owns the phone. We can define the inverse of a `hasOne` relationship using the `belongsTo` method: -->
이제 `User` 모델에서 `Phone` 모델을 접근할 수 있게 되었습니다. 반대로, `Phone` 모델에서도 이 전화기의 주인인 사용자를 접근할 수 있도록 연관관계를 정의해보겠습니다. `hasOne` 연관관계의 역방향은 `belongsTo` 메서드로 정의합니다:

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

<!-- When invoking the `user` method, Eloquent will attempt to find a `User` model that has an `id` which matches the `user_id` column on the `Phone` model. -->
`user` 메서드를 호출하면, Eloquent는 `Phone` 모델의 `user_id` 컬럼 값과 일치하는 `id`를 가진 `User` 모델을 찾으려고 시도합니다.

<!-- Eloquent determines the foreign key name by examining the name of the relationship method and suffixing the method name with `_id`. So, in this case, Eloquent assumes that the `Phone` model has a `user_id` column. However, if the foreign key on the `Phone` model is not `user_id`, you may pass a custom key name as the second argument to the `belongsTo` method: -->
Eloquent는 연관관계 메서드명을 참고해서 외래키 이름을 결정하고, 메서드명 뒤에 `_id`를 붙입니다. 즉, 위 예제에서 `Phone` 모델의 외래키는 `user_id`로 간주됩니다. 만약 `Phone` 모델의 외래키가 `user_id`가 아니라면, `belongsTo`의 두 번째 인수로 원하는 키 이름을 지정할 수 있습니다:

```php
/**
 * Get the user that owns the phone.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class, 'foreign_key');
}
```

<!-- If the parent model does not use `id` as its primary key, or you wish to find the associated model using a different column, you may pass a third argument to the `belongsTo` method specifying the parent table's custom key: -->
만약 부모 모델이 기본키로 `id`를 사용하지 않거나, 다른 컬럼으로 연관 모델을 찾고 싶다면, `belongsTo`의 세 번째 인수로 부모 테이블의 커스텀 키를 지정할 수 있습니다:

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
<!-- ### One to Many / Has Many -->
### One to Many / Has Many

<!-- A one-to-many relationship is used to define relationships where a single model is the parent to one or more child models. For example, a blog post may have an infinite number of comments. Like all other Eloquent relationships, one-to-many relationships are defined by defining a method on your Eloquent model: -->
일대다 연관관계는 한 모델이 여러 하위 모델을 소유할 때 사용합니다. 예를 들어, 블로그 게시글 하나에 무한히 많은 댓글이 달릴 수 있습니다. 다른 Eloquent 연관관계와 마찬가지로, 모델에 메서드로 정의합니다:

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

<!-- Remember, Eloquent will automatically determine the proper foreign key column for the `Comment` model. By convention, Eloquent will take the "snake case" name of the parent model and suffix it with `_id`. So, in this example, Eloquent will assume the foreign key column on the `Comment` model is `post_id`. -->
Eloquent는 `Comment` 모델의 외래키 컬럼명을 자동으로 판단합니다. 관례상, 부모 모델명을 스네이크 케이스로 한 뒤 `_id`를 붙입니다. 따라서 위 예제에서 `Comment` 모델의 외래키는 `post_id`로 간주됩니다.

<!-- Once the relationship method has been defined, we can access the [collection](/docs/12.x/eloquent-collections) of related comments by accessing the `comments` property. Remember, since Eloquent provides "dynamic relationship properties", we can access relationship methods as if they were defined as properties on the model: -->
연관관계 메서드를 정의하고 나면, `comments` 속성에 접근해서 [collection](/docs/12.x/eloquent-collections) 형태로 관련 댓글을 꺼내올 수 있습니다. Eloquent의 "동적 연관관계 속성" 덕분에 연관관계 메서드를 속성처럼 사용 가능합니다:

```php
use App\Models\Post;

$comments = Post::find(1)->comments;

foreach ($comments as $comment) {
    // ...
}
```

<!-- Since all relationships also serve as query builders, you may add further constraints to the relationship query by calling the `comments` method and continuing to chain conditions onto the query: -->
모든 연관관계는 쿼리 빌더 역할도 하므로, `comments` 메서드를 호출한 뒤 체이닝으로 조건을 더 추가할 수도 있습니다:

```php
$comment = Post::find(1)->comments()
    ->where('title', 'foo')
    ->first();
```

<!-- Like the `hasOne` method, you may also override the foreign and local keys by passing additional arguments to the `hasMany` method: -->
`hasOne`과 마찬가지로, `hasMany`에도 추가 인수로 외래키와 로컬키를 지정할 수 있습니다:

```php
return $this->hasMany(Comment::class, 'foreign_key');

return $this->hasMany(Comment::class, 'foreign_key', 'local_key');
```

<a name="automatically-hydrating-parent-models-on-children"></a>
<!-- #### Automatically Hydrating Parent Models on Children -->
#### Automatically Hydrating Parent Models on Children

<!-- Even when utilizing Eloquent eager loading, "N + 1" query problems can arise if you try to access the parent model from a child model while looping through the child models: -->
Eloquent의 즉시 로드를 사용하더라도, 하위 모델을 반복문으로 순회하는 도중에 해당 하위 모델에서 부모 모델에 접근하면 "N + 1" 쿼리 문제가 발생할 수 있습니다:

```php
$posts = Post::with('comments')->get();

foreach ($posts as $post) {
    foreach ($post->comments as $comment) {
        echo $comment->post->title;
    }
}
```

<!-- In the example above, an "N + 1" query problem has been introduced because, even though comments were eager loaded for every `Post` model, Eloquent does not automatically hydrate the parent `Post` on each child `Comment` model. -->
위 예제의 경우, 각 `Post` 모델마다 댓글은 즉시 로드했지만, 각각의 `Comment`에서 부모 `Post`를 자동으로 할당하지 않아서 "N + 1" 문제가 발생합니다.

<!-- If you would like Eloquent to automatically hydrate parent models onto their children, you may invoke the `chaperone` method when defining a `hasMany` relationship: -->
만약 Eloquent가 자식에 부모를 자동으로 할당하도록 하려면, `hasMany` 연관관계를 정의할 때 `chaperone` 메서드를 호출하십시오:

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

<!-- Or, if you would like to opt-in to automatic parent hydration at run time, you may invoke the `chaperone` model when eager loading the relationship: -->
혹은 런타임에 즉시 로드 시 `chaperone`을 사용해서 자동 부모 할당을 켤 수 있습니다:

```php
use App\Models\Post;

$posts = Post::with([
    'comments' => fn ($comments) => $comments->chaperone(),
])->get();
```

<a name="one-to-many-inverse"></a>
<!-- ### One to Many (Inverse) / Belongs To -->
### One to Many (Inverse) / Belongs To

<!-- Now that we can access all of a post's comments, let's define a relationship to allow a comment to access its parent post. To define the inverse of a `hasMany` relationship, define a relationship method on the child model which calls the `belongsTo` method: -->
이제 게시글의 모든 댓글을 조회할 수 있으니, 이번에는 댓글에서 부모 게시글에 접근하는 연관관계를 정의해보겠습니다. `hasMany` 연관관계의 역방향을 정의하려면 자식 모델에서 `belongsTo` 메서드를 활용한 연관관계 메서드를 정의합니다:

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

<!-- Once the relationship has been defined, we can retrieve a comment's parent post by accessing the `post` "dynamic relationship property": -->
연관관계를 정의한 뒤에는 `post` "동적 연관관계 속성"에 접근해 댓글의 부모 게시글을 가져올 수 있습니다:

```php
use App\Models\Comment;

$comment = Comment::find(1);

return $comment->post->title;
```

<!-- In the example above, Eloquent will attempt to find a `Post` model that has an `id` which matches the `post_id` column on the `Comment` model. -->
위 예제에서, Eloquent는 `Comment` 모델의 `post_id` 컬럼 값과 일치하는 `id`를 가진 `Post` 모델을 찾습니다.

<!-- Eloquent determines the default foreign key name by examining the name of the relationship method and suffixing the method name with a `_` followed by the name of the parent model's primary key column. So, in this example, Eloquent will assume the `Post` model's foreign key on the `comments` table is `post_id`. -->
Eloquent는 연관관계 메서드명의 뒤에 `_`와 부모 모델의 기본키명을 이어 붙여, 외래키명을 결정합니다. 예를 들어, 위에서 `comments` 테이블에 대한 `Post` 모델의 외래키는 `post_id`입니다.

<!-- However, if the foreign key for your relationship does not follow these conventions, you may pass a custom foreign key name as the second argument to the `belongsTo` method: -->
만약 외래키 규칙이 다르다면, `belongsTo`에 두 번째 인수로 커스텀 외래키명을 넘길 수 있습니다:

```php
/**
 * Get the post that owns the comment.
 */
public function post(): BelongsTo
{
    return $this->belongsTo(Post::class, 'foreign_key');
}
```

<!-- If your parent model does not use `id` as its primary key, or you wish to find the associated model using a different column, you may pass a third argument to the `belongsTo` method specifying your parent table's custom key: -->
부모 모델이 `id`외의 다른 컬럼을 기본키로 사용하거나, 연관 모델 찾을 컬럼이 다르다면 `belongsTo`의 세 번째 인수로 커스텀 키를 지정하세요:

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
<!-- #### Default Models -->
#### Default Models

<!-- The `belongsTo`, `hasOne`, `hasOneThrough`, and `morphOne` relationships allow you to define a default model that will be returned if the given relationship is `null`. This pattern is often referred to as the [Null Object pattern](https://en.wikipedia.org/wiki/Null_Object_pattern) and can help remove conditional checks in your code. In the following example, the `user` relation will return an empty `App\Models\User` model if no user is attached to the `Post` model: -->
`belongsTo`, `hasOne`, `hasOneThrough`, `morphOne` 연관관계에서는 만약 연관된 모델이 `null`일 때 반환할 기본 모델을 정의할 수 있습니다. 이 패턴은 [Null Object pattern](https://en.wikipedia.org/wiki/Null_Object_pattern)이라고 불리며, 코드 내 조건문을 줄이는 데 도움이 됩니다. 아래 예제는 `Post` 모델에 사용자가 연결되지 않은 경우 `user` 연관관계가 비어 있는 `App\Models\User` 모델을 반환합니다:

```php
/**
 * Get the author of the post.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault();
}
```

<!-- To populate the default model with attributes, you may pass an array or closure to the `withDefault` method: -->
기본 모델에 속성을 채워 넣으려면, `withDefault`에 배열 또는 클로저를 넘기면 됩니다:

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
<!-- #### Querying Belongs To Relationships -->
#### Querying Belongs To Relationships

<!-- When querying for the children of a "belongs to" relationship, you may manually build the `where` clause to retrieve the corresponding Eloquent models: -->
"belongs to" 연관관계의 하위 항목을 쿼리할 때, `where` 절을 직접 작성할 수 있습니다:

```php
use App\Models\Post;

$posts = Post::where('user_id', $user->id)->get();
```

<!-- However, you may find it more convenient to use the `whereBelongsTo` method, which will automatically determine the proper relationship and foreign key for the given model: -->
더 편리하게 사용하려면, 주어진 모델 기준으로 관계와 외래키를 자동으로 판단하는 `whereBelongsTo` 메서드를 이용하세요:

```php
$posts = Post::whereBelongsTo($user)->get();
```

<!-- You may also provide a [collection](/docs/12.x/eloquent-collections) instance to the `whereBelongsTo` method. When doing so, Laravel will retrieve models that belong to any of the parent models within the collection: -->
`whereBelongsTo` 메서드에는 [collection](/docs/12.x/eloquent-collections)를 넘겨 여러 부모 모델을 대상으로 할 수 있습니다:

```php
$users = User::where('vip', true)->get();

$posts = Post::whereBelongsTo($users)->get();
```

<!-- By default, Laravel will determine the relationship associated with the given model based on the class name of the model; however, you may specify the relationship name manually by providing it as the second argument to the `whereBelongsTo` method: -->
Laravel은 기본적으로 주어진 모델의 클래스 이름을 바탕으로 연관관계를 판단하지만, `whereBelongsTo` 메서드의 두 번째 인수로 관계명을 직접 지정할 수도 있습니다:

```php
$posts = Post::whereBelongsTo($user, 'author')->get();
```

<a name="has-one-of-many"></a>
<!-- ### Has One of Many -->
### Has One of Many

<!-- Sometimes a model may have many related models, yet you want to easily retrieve the "latest" or "oldest" related model of the relationship. For example, a `User` model may be related to many `Order` models, but you want to define a convenient way to interact with the most recent order the user has placed. You may accomplish this using the `hasOne` relationship type combined with the `ofMany` methods: -->
종종 한 모델이 여러 개의 연관된 모델을 가질 수 있지만, 이 중에서 "가장 최신" 또는 "가장 오래된" 모델만 쉽게 가져오고 싶을 수 있습니다. 예를 들어, `User`가 여러개의 `Order`와 연관되어 있지만 사용자가 가장 최근에 주문한 주문만 가져오고 싶을 때가 있습니다. 이럴 때는 `hasOne` 연관관계와 `ofMany` 계열 메서드를 조합해서 처리할 수 있습니다:

```php
/**
 * Get the user's most recent order.
 */
public function latestOrder(): HasOne
{
    return $this->hasOne(Order::class)->latestOfMany();
}
```

<!-- Likewise, you may define a method to retrieve the "oldest", or first, related model of a relationship: -->
마찬가지로 "가장 오래된" 연관 모델을 가져오는 메서드도 정의할 수 있습니다:

```php
/**
 * Get the user's oldest order.
 */
public function oldestOrder(): HasOne
{
    return $this->hasOne(Order::class)->oldestOfMany();
}
```

<!-- By default, the `latestOfMany` and `oldestOfMany` methods will retrieve the latest or oldest related model based on the model's primary key, which must be sortable. However, sometimes you may wish to retrieve a single model from a larger relationship using a different sorting criteria. -->
기본적으로 `latestOfMany`와 `oldestOfMany` 메서드는 정렬 가능해야 하는 모델의 기본키(primary key)를 기준으로 가장 최신 또는 가장 오래된 관련 모델을 조회합니다. 하지만 때로는 다른 정렬 기준을 사용해 더 큰 연관관계에서 단일 모델을 조회하고 싶을 수 있습니다.

<!-- For example, using the `ofMany` method, you may retrieve the user's most expensive order. The `ofMany` method accepts the sortable column as its first argument and which aggregate function (`min` or `max`) to apply when querying for the related model: -->
예를 들어, `ofMany` 메서드를 사용하면 사용자의 가장 비싼 주문을 조회할 수 있습니다. `ofMany` 메서드는 첫 번째 인수로 정렬할 컬럼을 받고, 관련 모델을 쿼리할 때 적용할 집계 함수(`min` 또는 `max`)를 받습니다:

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
> PostgreSQL은 UUID 컬럼에 대해 `MAX` 함수를 사용할 수 없으므로, PostgreSQL UUID 컬럼과 one-of-many 관계는 함께 사용할 수 없습니다.

<a name="converting-many-relationships-to-has-one-relationships"></a>
<!-- #### Converting "Many" Relationships to Has One Relationships -->
#### Converting "Many" Relationships to Has One Relationships

<!-- Often, when retrieving a single model using the `latestOfMany`, `oldestOfMany`, or `ofMany` methods, you already have a "has many" relationship defined for the same model. For convenience, Laravel allows you to easily convert this relationship into a "has one" relationship by invoking the `one` method on the relationship: -->
이미 `latestOfMany`, `oldestOfMany`, `ofMany` 메서드로 1개만 뽑아오는 상황이라면, 기존의 "has many" 연관관계를 쉽게 "has one"으로 변환할 수 있습니다. 관계에서 `one` 메서드를 호출하면 됩니다:

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

<!-- You may also use the `one` method to convert `HasManyThrough` relationships to `HasOneThrough` relationships: -->
`one` 메서드는 `HasManyThrough`를 `HasOneThrough`로 바꿀 때도 사용할 수 있습니다:

```php
public function latestDeployment(): HasOneThrough
{
    return $this->deployments()->one()->latestOfMany();
}
```

<a name="advanced-has-one-of-many-relationships"></a>
<!-- #### Advanced Has One of Many Relationships -->
#### Advanced Has One of Many Relationships

<!-- It is possible to construct more advanced "has one of many" relationships. For example, a `Product` model may have many associated `Price` models that are retained in the system even after new pricing is published. In addition, new pricing data for the product may be able to be published in advance to take effect at a future date via a `published_at` column. -->
더 복잡한 "has one of many" 연관관계를 구성할 수도 있습니다. 예를 들어, `Product` 모델이 여러 개의 `Price` 모델과 연관되어 있고, 새 가격이 공개된 뒤에도 기존 가격을 시스템에 보관한다고 합시다. 또한 `published_at` 컬럼을 통해 제품의 새 가격 데이터를 미리 공개해 미래의 특정 시점에 적용되도록 할 수도 있습니다.

<!-- So, in summary, we need to retrieve the latest published pricing where the published date is not in the future. In addition, if two prices have the same published date, we will prefer the price with the greatest ID. To accomplish this, we must pass an array to the `ofMany` method that contains the sortable columns which determine the latest price. In addition, a closure will be provided as the second argument to the `ofMany` method. This closure will be responsible for adding additional publish date constraints to the relationship query: -->
요약하면, 미래가 아닌 공개일 중 가장 최신 공개 가격을 가져와야 합니다. 또한 공개일이 같은 가격이 둘 이상이면 ID가 가장 큰 가격을 우선합니다. 이를 위해 최신 가격을 결정하는 정렬 가능 컬럼들을 담은 배열을 `ofMany` 메서드에 전달해야 합니다. 또한 `ofMany` 메서드의 두 번째 인수로 클로저를 전달합니다. 이 클로저는 연관관계 쿼리에 추가 공개일 조건을 더하는 역할을 합니다:

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
<!-- ### Has One Through -->
### Has One Through

<!-- The "has-one-through" relationship defines a one-to-one relationship with another model. However, this relationship indicates that the declaring model can be matched with one instance of another model by proceeding _through_ a third model. -->
"has-one-through" 연관관계는 다른 모델과의 일대일 관계이지만, 이 관계는 _중간_ 모델을 거쳐 연관됩니다.

<!-- For example, in a vehicle repair shop application, each `Mechanic` model may be associated with one `Car` model, and each `Car` model may be associated with one `Owner` model. While the mechanic and the owner have no direct relationship within the database, the mechanic can access the owner _through_ the `Car` model. Let's look at the tables necessary to define this relationship: -->
예를 들어, 차량 정비소 앱에서 `Mechanic`(정비사)마다 한 대의 `Car`(자동차)가 연관되어 있고, 각 `Car`마다 `Owner`(차주)가 있습니다. 이 때, 정비사와 차주 사이에는 직접적인 관계가 없지만, `Car`를 통해 접근이 가능합니다. 아래는 이 관계를 정의하기 위한 테이블 구조입니다:

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

<!-- Now that we have examined the table structure for the relationship, let's define the relationship on the `Mechanic` model: -->
이 테이블 구조에 따라 `Mechanic` 모델에 연관관계를 정의하면 다음과 같습니다:

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

<!-- The first argument passed to the `hasOneThrough` method is the name of the final model we wish to access, while the second argument is the name of the intermediate model. -->
`hasOneThrough`의 첫 번째 인수는 최종적으로 접근할 모델, 두 번째 인수는 중간 모델입니다.

<!-- Or, if the relevant relationships have already been defined on all of the models involved in the relationship, you may fluently define a "has-one-through" relationship by invoking the `through` method and supplying the names of those relationships. For example, if the `Mechanic` model has a `cars` relationship and the `Car` model has an `owner` relationship, you may define a "has-one-through" relationship connecting the mechanic and the owner like so: -->
또는, 연관된 모든 모델에 이미 관계가 정의되어 있다면, `Mechanic` 모델에서 `cars` 관계를 거쳐 `Car` 모델의 `owner` 관계로 이어지도록 `through` 메서드와 관계명을 조합해 조금 더 유연하게 "has-one-through"를 정의할 수 있습니다:

```php
// String based syntax...
return $this->through('cars')->has('owner');

// Dynamic syntax...
return $this->throughCars()->hasOwner();
```

<a name="has-one-through-key-conventions"></a>
<!-- #### Key Conventions -->
#### Key Conventions

<!-- Typical Eloquent foreign key conventions will be used when performing the relationship's queries. If you would like to customize the keys of the relationship, you may pass them as the third and fourth arguments to the `hasOneThrough` method. The third argument is the name of the foreign key on the intermediate model. The fourth argument is the name of the foreign key on the final model. The fifth argument is the local key, while the sixth argument is the local key of the intermediate model: -->
Eloquent의 외래키 규칙이 기본적으로 적용됩니다. 키를 직접 지정하려면, `hasOneThrough`의 3-6번째 인수로 각각 중간 모델의 외래키명, 최종 모델의 외래키명, mechanics 테이블의 로컬키, cars 테이블의 로컬키를 지정할 수 있습니다:

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

<!-- Or, as discussed earlier, if the relevant relationships have already been defined on all of the models involved in the relationship, you may fluently define a "has-one-through" relationship by invoking the `through` method and supplying the names of those relationships. This approach offers the advantage of reusing the key conventions already defined on the existing relationships: -->
앞서 설명한 것처럼, 각 모델에 이미 연관관계가 정의되어 있다면 `through` 메서드를 사용해 키 규칙도 재사용할 수 있습니다:

```php
// String based syntax...
return $this->through('cars')->has('owner');

// Dynamic syntax...
return $this->throughCars()->hasOwner();
```

<a name="has-many-through"></a>
<!-- ### Has Many Through -->
### Has Many Through

<!-- The "has-many-through" relationship provides a convenient way to access distant relations via an intermediate relation. For example, let's assume we are building a deployment platform like [Laravel Cloud](https://cloud.laravel.com). An `Application` model might access many `Deployment` models through an intermediate `Environment` model. Using this example, you could easily gather all deployments for a given application. Let's look at the tables required to define this relationship: -->
"has-many-through" 연관관계는 간접적인 관계로 멀리 있는 모델을 쉽게 접근할 수 있게 합니다. 예를 들어, [Laravel Cloud](https://cloud.laravel.com)와 같은 배포 플랫폼에서 `Application` 모델을 기준으로 중간에 `Environment`(환경) 모델을 거쳐 다수의 `Deployment`(배포)를 가져와야 할 수 있습니다. 이 때 테이블 구조는 다음과 같을 수 있습니다:

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

<!-- Now that we have examined the table structure for the relationship, let's define the relationship on the `Application` model: -->
이 구조에서, `Application` 모델에 아래처럼 연관관계를 정의할 수 있습니다:

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

<!-- The first argument passed to the `hasManyThrough` method is the name of the final model we wish to access, while the second argument is the name of the intermediate model. -->
`hasManyThrough` 메서드의 첫 번째 인수는 최종적으로 접근할 모델, 두 번째 인수는 중간 모델입니다.

<!-- Or, if the relevant relationships have already been defined on all of the models involved in the relationship, you may fluently define a "has-many-through" relationship by invoking the `through` method and supplying the names of those relationships. For example, if the `Application` model has a `environments` relationship and the `Environment` model has a `deployments` relationship, you may define a "has-many-through" relationship connecting the application and the deployments like so: -->
또한, 이미 각 모델에 관계가 정의되어 있다면 `Application` 모델에서 `environments` 관계를 거쳐 `Environment` 모델의 `deployments` 관계로 이어지도록 `through` 메서드를 사용해 다음처럼 유연하게 정의할 수 있습니다:

```php
// String based syntax...
return $this->through('environments')->has('deployments');

// Dynamic syntax...
return $this->throughEnvironments()->hasDeployments();
```

<!-- Though the `Deployment` model's table does not contain a `application_id` column, the `hasManyThrough` relation provides access to an application's deployments via `$application->deployments`. To retrieve these models, Eloquent inspects the `application_id` column on the intermediate `Environment` model's table. After finding the relevant environment IDs, they are used to query the `Deployment` model's table. -->
`Deployment` 모델의 테이블에는 `application_id` 컬럼이 없지만, `hasManyThrough` 관계는 `$application->deployments`를 통해 애플리케이션의 `Deployment` 모델에 접근할 수 있게 해줍니다. 이를 위해 Eloquent는 중간 `Environment` 테이블의 `application_id` 컬럼을 검사합니다.

<a name="has-many-through-key-conventions"></a>
<!-- #### Key Conventions -->
#### Key Conventions

<!-- Typical Eloquent foreign key conventions will be used when performing the relationship's queries. If you would like to customize the keys of the relationship, you may pass them as the third and fourth arguments to the `hasManyThrough` method. The third argument is the name of the foreign key on the intermediate model. The fourth argument is the name of the foreign key on the final model. The fifth argument is the local key, while the sixth argument is the local key of the intermediate model: -->
Eloquent 기본값을 사용하지 않고, 직접 키를 지정하려면 `hasManyThrough`의 3-6번째 인수로 다음을 전달하세요:

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

<!-- Or, as discussed earlier, if the relevant relationships have already been defined on all of the models involved in the relationship, you may fluently define a "has-many-through" relationship by invoking the `through` method and supplying the names of those relationships. This approach offers the advantage of reusing the key conventions already defined on the existing relationships: -->
이미 각각 관계가 정의된 경우에는 `through` 메서드를 통해 기존의 키 규칙이 재사용됩니다:

```php
// String based syntax...
return $this->through('environments')->has('deployments');

// Dynamic syntax...
return $this->throughEnvironments()->hasDeployments();
```

<a name="scoped-relationships"></a>
<!-- ### Scoped Relationships -->
### Scoped Relationships

<!-- It's common to add additional methods to models that constrain relationships. For example, you might add a `featuredPosts` method to a `User` model which constrains the broader `posts` relationship with an additional `where` constraint: -->
모델에서 특정 연관관계에 제약조건(스코프)를 적용한 메서드를 추가하는 경우가 많습니다. 예를 들어, `User` 모델에서 `posts` 연관관계에 추가적인 `where` 조건을 걸어서 `featuredPosts` 메서드를 만들 수 있습니다:

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

<!-- However, if you attempt to create a model via the `featuredPosts` method, its `featured` attribute would not be set to `true`. If you would like to create models via relationship methods and also specify attributes that should be added to all models created via that relationship, you may use the `withAttributes` method when building the relationship query: -->
하지만, 위와 같이 `featuredPosts`로 모델을 생성하면 해당 모델의 `featured` 속성이 자동으로 `true`로 지정되지는 않습니다. 연관관계 메서드로 모델을 생성하면서 특정 속성까지 포함시키려면, 쿼리 빌드 시 `withAttributes`를 사용할 수 있습니다:

```php
/**
 * Get the user's featured posts.
 */
public function featuredPosts(): HasMany
{
    return $this->posts()->withAttributes(['featured' => true]);
}
```

<!-- The `withAttributes` method will add `where` conditions to the query using the given attributes, and it will also add the given attributes to any models created via the relationship method: -->
`withAttributes`는 쿼리의 `where` 조건에도 해당 속성을 조건으로 추가하고, 새 모델을 생성할 때도 포함합니다:

```php
$post = $user->featuredPosts()->create(['title' => 'Featured Post']);

$post->featured; // true
```

<!-- To instruct the `withAttributes` method to not add `where` conditions to the query, you may set the `asConditions` argument to `false`: -->
`withAttributes` 메서드가 쿼리에 `where` 조건을 추가하지 않게 하고 속성만 추가하고 싶다면, `asConditions` 인수를 `false`로 지정하세요:

```php
return $this->posts()->withAttributes(['featured' => true], asConditions: false);
```

<a name="many-to-many"></a>
<!-- ## Many to Many Relationships -->
## Many to Many Relationships

<!-- Many-to-many relations are slightly more complicated than `hasOne` and `hasMany` relationships. An example of a many-to-many relationship is a user that has many roles and those roles are also shared by other users in the application. For example, a user may be assigned the role of "Author" and "Editor"; however, those roles may also be assigned to other users as well. So, a user has many roles and a role has many users. -->
다대다 연관관계는 `hasOne`, `hasMany`에 비해 조금 복잡합니다. 대표적인 예로, 하나의 사용자가 여러 역할(role)을 가질 수 있고, 하나의 역할이 여러 사용자에게 공유될 수도 있습니다. 즉, 한 사용자가 "Author", "Editor" 역할을 동시에 가질 수 있고, 각각의 역할은 다른 사용자에게도 할당될 수 있습니다.

<a name="many-to-many-table-structure"></a>
<!-- #### Table Structure -->
#### Table Structure

<!-- To define this relationship, three database tables are needed: `users`, `roles`, and `role_user`. The `role_user` table is derived from the alphabetical order of the related model names and contains `user_id` and `role_id` columns. This table is used as an intermediate table linking the users and roles. -->
다대다 연관관계에는 보통 `users`, `roles`, `role_user` 세 개의 테이블이 필요합니다. 중간 테이블인 `role_user`는 알파벳 순서로 처리된 관계 모델명에서 유래되며, `user_id`와 `role_id` 컬럼을 가집니다. 이 테이블이 users와 roles를 연결해줍니다.

<!-- Remember, since a role can belong to many users, we cannot simply place a `user_id` column on the `roles` table. This would mean that a role could only belong to a single user. In order to provide support for roles being assigned to multiple users, the `role_user` table is needed. We can summarize the relationship's table structure like so: -->
기억하세요. 하나의 역할은 여러 사용자에게 속할 수 있으므로, `roles` 테이블에 단순히 `user_id` 컬럼을 둘 수는 없습니다. 그렇게 하면 하나의 역할이 단 한 명의 사용자에게만 속할 수 있게 됩니다. 여러 사용자에게 역할을 할당할 수 있도록 지원하려면 `role_user` 테이블이 필요합니다. 이 연관관계의 테이블 구조는 다음과 같이 요약할 수 있습니다:

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
<!-- #### Model Structure -->
#### Model Structure

<!-- Many-to-many relationships are defined by writing a method that returns the result of the `belongsToMany` method. The `belongsToMany` method is provided by the `Illuminate\Database\Eloquent\Model` base class that is used by all of your application's Eloquent models. For example, let's define a `roles` method on our `User` model. The first argument passed to this method is the name of the related model class: -->
다대다 연관관계는 `belongsToMany` 메서드의 결과를 반환하는 메서드를 작성하면 됩니다. `belongsToMany` 메서드는 모든 Eloquent 모델의 부모인 `Illuminate\Database\Eloquent\Model`에서 제공됩니다. 아래는 `User` 모델의 `roles` 메서드 예시입니다:

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

<!-- Once the relationship is defined, you may access the user's roles using the `roles` dynamic relationship property: -->
관계가 정의되고 나면, `roles` 동적 연관관계 속성으로 사용자의 역할 목록에 접근할 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

foreach ($user->roles as $role) {
    // ...
}
```

<!-- Since all relationships also serve as query builders, you may add further constraints to the relationship query by calling the `roles` method and continuing to chain conditions onto the query: -->
연관관계도 쿼리 빌더이므로, `roles` 메서드를 호출하고 조건을 체이닝해서 추출할 수 있습니다:

```php
$roles = User::find(1)->roles()->orderBy('name')->get();
```

<!-- To determine the table name of the relationship's intermediate table, Eloquent will join the two related model names in alphabetical order. However, you are free to override this convention. You may do so by passing a second argument to the `belongsToMany` method: -->
관계 중간 테이블의 이름은 관련 모델명을 알파벳순으로 조합합니다. 이 규칙은 `belongsToMany` 메서드의 두 번째 인수로 직접 지정할 수도 있습니다:

```php
return $this->belongsToMany(Role::class, 'role_user');
```

<!-- In addition to customizing the name of the intermediate table, you may also customize the column names of the keys on the table by passing additional arguments to the `belongsToMany` method. The third argument is the foreign key name of the model on which you are defining the relationship, while the fourth argument is the foreign key name of the model that you are joining to: -->
중간 테이블의 키 컬럼명도 `belongsToMany` 메서드의 3, 4번째 인수로 지정 가능합니다(자기 자신의 외래키, 반대 모델의 외래키):

```php
return $this->belongsToMany(Role::class, 'role_user', 'user_id', 'role_id');
```

<a name="many-to-many-defining-the-inverse-of-the-relationship"></a>
<!-- #### Defining the Inverse of the Relationship -->
#### Defining the Inverse of the Relationship

<!-- To define the "inverse" of a many-to-many relationship, you should define a method on the related model which also returns the result of the `belongsToMany` method. To complete our user / role example, let's define the `users` method on the `Role` model: -->
다대다 연관관계의 "역방향"을 정의하려면, 관련 모델에도 역시 `belongsToMany`를 반환하는 메서드를 작성하면 됩니다. 이제 `Role` 모델에도 `users` 관계를 추가해봅니다:

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

<!-- As you can see, the relationship is defined exactly the same as its `User` model counterpart with the exception of referencing the `App\Models\User` model. Since we're reusing the `belongsToMany` method, all of the usual table and key customization options are available when defining the "inverse" of many-to-many relationships. -->
사용법/옵션/커스텀화는 `User` 모델에서 `App\Models\User` 모델을 참조한다는 점만 제외하면 동일하며, `belongsToMany` 메서드를 재사용하므로 일반적인 테이블 및 키 커스터마이징 옵션도 모두 사용할 수 있습니다.

<a name="retrieving-intermediate-table-columns"></a>
<!-- ### Retrieving Intermediate Table Columns -->
### Retrieving Intermediate Table Columns

<!-- As you have already learned, working with many-to-many relations requires the presence of an intermediate table. Eloquent provides some very helpful ways of interacting with this table. For example, let's assume our `User` model has many `Role` models that it is related to. After accessing this relationship, we may access the intermediate table using the `pivot` attribute on the models: -->
다대다 연관관계에서는 중간 테이블이 필요합니다. Eloquent는 이 테이블과 쉽게 상호작용할 수 있게 도와줍니다. 예를 들어, `User`가 여러 `Role`과 연결되어 있을 때 각 역할의 `pivot` 속성을 통해 중간 테이블 정보에 접근 가능합니다:

```php
use App\Models\User;

$user = User::find(1);

foreach ($user->roles as $role) {
    echo $role->pivot->created_at;
}
```

<!-- Notice that each `Role` model we retrieve is automatically assigned a `pivot` attribute. This attribute contains a model representing the intermediate table. -->
조회한 각 `Role` 모델에는 `pivot` 속성이 자동으로 할당됩니다. 이 속성은 중간 테이블을 나타내는 모델입니다.

<!-- By default, only the model keys will be present on the `pivot` model. If your intermediate table contains extra attributes, you must specify them when defining the relationship: -->
기본적으로 `pivot` 모델에는 모델 키만 포함됩니다. 중간 테이블에 추가 속성이 있다면 연관관계를 정의할 때 명시해야 합니다:

```php
return $this->belongsToMany(Role::class)->withPivot('active', 'created_by');
```

<!-- If you would like your intermediate table to have `created_at` and `updated_at` timestamps that are automatically maintained by Eloquent, call the `withTimestamps` method when defining the relationship: -->
`created_at`, `updated_at` 등 타임스탬프를 자동으로 관리하고 싶으면 연관관계를 정의할 때 `withTimestamps` 메서드를 호출하세요:

```php
return $this->belongsToMany(Role::class)->withTimestamps();
```

> [!WARNING]
> Eloquent의 자동 타임스탬프를 사용할 때에는 반드시 `created_at`와 `updated_at` 컬럼이 모두 존재해야 합니다.

<a name="customizing-the-pivot-attribute-name"></a>
<!-- #### Customizing the `pivot` Attribute Name -->
#### Customizing the `pivot` Attribute Name

<!-- As noted previously, attributes from the intermediate table may be accessed on models via the `pivot` attribute. However, you are free to customize the name of this attribute to better reflect its purpose within your application. -->
앞서 설명했듯이 중간 테이블의 속성은 모델에서 `pivot` 속성을 통해 접근할 수 있습니다. 하지만 이 속성명을 애플리케이션 내에서의 용도를 더 잘 나타내도록 자유롭게 변경할 수 있습니다.

<!-- For example, if your application contains users that may subscribe to podcasts, you likely have a many-to-many relationship between users and podcasts. If this is the case, you may wish to rename your intermediate table attribute to `subscription` instead of `pivot`. This can be done using the `as` method when defining the relationship: -->
예를 들어 사용자가 팟캐스트를 구독할 수 있는 애플리케이션이라면, 사용자와 팟캐스트 사이에 다대다 연관관계가 있을 것입니다. 이런 경우 중간 테이블 속성명을 `pivot` 대신 `subscription`으로 바꾸고 싶을 수 있습니다. 이는 관계를 정의할 때 `as` 메서드로 할 수 있습니다:

```php
return $this->belongsToMany(Podcast::class)
    ->as('subscription')
    ->withTimestamps();
```

<!-- Once the custom intermediate table attribute has been specified, you may access the intermediate table data using the customized name: -->
이후에는 커스텀 속성명으로 접근하면 됩니다:

```php
$users = User::with('podcasts')->get();

foreach ($users->flatMap->podcasts as $podcast) {
    echo $podcast->subscription->created_at;
}
```

<a name="filtering-queries-via-intermediate-table-columns"></a>
<!-- ### Filtering Queries via Intermediate Table Columns -->
### Filtering Queries via Intermediate Table Columns

<!-- You can also filter the results returned by `belongsToMany` relationship queries using the `wherePivot`, `wherePivotIn`, `wherePivotNotIn`, `wherePivotBetween`, `wherePivotNotBetween`, `wherePivotNull`, and `wherePivotNotNull` methods when defining the relationship: -->
`belongsToMany` 관계 쿼리가 반환하는 결과를 중간 테이블 값을 조건으로 필터링할 수도 있습니다. 다음 메서드를 사용할 수 있습니다: `wherePivot`, `wherePivotIn`, `wherePivotNotIn`, `wherePivotBetween`, `wherePivotNotBetween`, `wherePivotNull`, `wherePivotNotNull`

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

<!-- The `wherePivot` adds a where clause constraint to the query, but does not add the specified value when creating new models via the defined relationship. If you need to both query and create relationships with a particular pivot value, you may use the `withPivotValue` method: -->
`wherePivot`은 쿼리에 WHERE 조건만 추가하며, 새 모델 생성 시에는 해당 값을 세팅하지 않습니다. 둘 다 적용하려면, `withPivotValue`를 사용합니다:

```php
return $this->belongsToMany(Role::class)
    ->withPivotValue('approved', 1);
```

<a name="ordering-queries-via-intermediate-table-columns"></a>
<!-- ### Ordering Queries via Intermediate Table Columns -->
### Ordering Queries via Intermediate Table Columns

<!-- You can order the results returned by `belongsToMany` relationship queries using the `orderByPivot` and `orderByPivotDesc` methods. In the following example, we will retrieve all of the latest badges for the user: -->
`belongsToMany` 관계 쿼리가 반환하는 결과는 `orderByPivot` 및 `orderByPivotDesc`로 중간 테이블 컬럼 기준으로 정렬할 수 있습니다:

```php
return $this->belongsToMany(Badge::class)
    ->where('rank', 'gold')
    ->orderByPivotDesc('created_at');
```

<a name="defining-custom-intermediate-table-models"></a>
<!-- ### Defining Custom Intermediate Table Models -->
### Defining Custom Intermediate Table Models

<!-- If you would like to define a custom model to represent the intermediate table of your many-to-many relationship, you may call the `using` method when defining the relationship. Custom pivot models give you the opportunity to define additional behavior on the pivot model, such as methods and casts. -->
다대다 연관관계의 중간 테이블에 대한 커스텀 모델을 만들고 싶다면 `using` 메서드로 지정하세요. 커스텀 pivot 모델을 통해 추가 동작(메서드, cast 등)을 정의할 수 있습니다.

<!-- Custom many-to-many pivot models should extend the `Illuminate\Database\Eloquent\Relations\Pivot` class while custom polymorphic many-to-many pivot models should extend the `Illuminate\Database\Eloquent\Relations\MorphPivot` class. For example, we may define a `Role` model which uses a custom `RoleUser` pivot model: -->
커스텀 다대다 pivot 모델은 `Illuminate\Database\Eloquent\Relations\Pivot` 클래스를 상속해야 하며, 커스텀 다형성 다대다 pivot 모델은 `Illuminate\Database\Eloquent\Relations\MorphPivot` 클래스를 상속해야 합니다. 예를 들어, 커스텀 `RoleUser` pivot 모델을 사용하는 `Role` 모델을 다음처럼 정의할 수 있습니다:

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

<!-- When defining the `RoleUser` model, you should extend the `Illuminate\Database\Eloquent\Relations\Pivot` class: -->
`RoleUser` 모델을 정의할 때는 `Illuminate\Database\Eloquent\Relations\Pivot` 클래스를 상속해야 합니다:

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
> Pivot 모델은 `SoftDeletes` 트레잇을 사용할 수 없습니다. Pivot 레코드에 soft delete가 필요하면, 일반 Eloquent 모델로 전환하는 것이 좋습니다.

<a name="custom-pivot-models-and-incrementing-ids"></a>
<!-- #### Custom Pivot Models and Incrementing IDs -->
#### Custom Pivot Models and Incrementing IDs

<!-- If you have defined a many-to-many relationship that uses a custom pivot model, and that pivot model has an auto-incrementing primary key, you should ensure your custom pivot model class defines an `incrementing` property that is set to `true`. -->
커스텀 pivot 모델에서 자동 증가 primary key를 사용한다면, 커스텀 pivot 모델 클래스에 `true`로 설정된 `incrementing` 속성을 반드시 선언해야 합니다:

```php
/**
 * Indicates if the IDs are auto-incrementing.
 *
 * @var bool
 */
public $incrementing = true;
```

<a name="polymorphic-relationships"></a>
<!-- ## Polymorphic Relationships -->
## Polymorphic Relationships

<!-- A polymorphic relationship allows the child model to belong to more than one type of model using a single association. For example, imagine you are building an application that allows users to share blog posts and videos. In such an application, a `Comment` model might belong to both the `Post` and `Video` models. -->
다형성(polymorphic) 연관관계는 하위 모델이 단일 연관으로 둘 이상의 모델 타입에 속할 수 있게 해줍니다. 예를 들어, 사용자가 블로그 게시글과 동영상을 공유하는 앱에서 `Comment` 모델은 `Post` 모델과 `Video` 모델 모두에 속할 수 있습니다.

<a name="one-to-one-polymorphic-relations"></a>
<!-- ### One to One (Polymorphic) -->
### One to One (Polymorphic)

<a name="one-to-one-polymorphic-table-structure"></a>
<!-- #### Table Structure -->
#### Table Structure

<!-- A one-to-one polymorphic relation is similar to a typical one-to-one relation; however, the child model can belong to more than one type of model using a single association. For example, a blog `Post` and a `User` may share a polymorphic relation to an `Image` model. Using a one-to-one polymorphic relation allows you to have a single table of unique images that may be associated with posts and users. First, let's examine the table structure: -->
일대일 다형성 연관관계는 일반적인 일대일과 유사하지만, 자식 모델이 하나의 연관으로 여러 타입의 모델에 속할 수 있다는 점이 다릅니다. 예를 들어, `Post`와 `User`가 `Image` 모델과 다형성 관계를 공유할 수 있습니다. 하나의 고유한 이미지 테이블로 게시글과 사용자 모두에 연결 가능합니다. 테이블 구조는 다음과 같습니다:

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

<!-- Note the `imageable_id` and `imageable_type` columns on the `images` table. The `imageable_id` column will contain the ID value of the post or user, while the `imageable_type` column will contain the class name of the parent model. The `imageable_type` column is used by Eloquent to determine which "type" of parent model to return when accessing the `imageable` relation. In this case, the column would contain either `App\Models\Post` or `App\Models\User`. -->
`images` 테이블의 `imageable_id`와 `imageable_type` 컬럼에 주목하세요. `imageable_id` 컬럼은 게시글 또는 사용자의 ID 값을, `imageable_type` 컬럼은 부모 모델의 클래스명을 담고 있습니다. Eloquent는 `imageable_type` 컬럼을 통해 `imageable` 관계에 접근할 때 반환할 부모 모델의 "타입"을 결정합니다. 이 컬럼에는 `App\Models\Post` 또는 `App\Models\User` 같은 값이 들어갑니다.

<a name="one-to-one-polymorphic-model-structure"></a>
<!-- #### Model Structure -->
#### Model Structure

<!-- Next, let's examine the model definitions needed to build this relationship: -->
이 관계를 구성하기 위한 모델 정의는 다음과 같습니다:

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
<!-- #### Retrieving the Relationship -->
#### Retrieving the Relationship

<!-- Once your database table and models are defined, you may access the relationships via your models. For example, to retrieve the image for a post, we can access the `image` dynamic relationship property: -->
데이터베이스 테이블과 모델이 정의되면, 모델을 통해 연관관계에 접근할 수 있습니다. 예를 들어, 게시글의 이미지를 가져오려면 `image` 동적 연관관계 속성에 접근하면 됩니다:

```php
use App\Models\Post;

$post = Post::find(1);

$image = $post->image;
```

<!-- You may retrieve the parent of the polymorphic model by accessing the name of the method that performs the call to `morphTo`. In this case, that is the `imageable` method on the `Image` model. So, we will access that method as a dynamic relationship property: -->
`morphTo`를 호출하는 메서드명에 접근하면 다형성 모델의 부모를 조회할 수 있습니다. 이 경우 `Image` 모델의 `imageable` 메서드입니다. 이를 동적 연관관계 속성으로 접근합니다:

```php
use App\Models\Image;

$image = Image::find(1);

$imageable = $image->imageable;
```

<!-- The `imageable` relation on the `Image` model will return either a `Post` or `User` instance, depending on which type of model owns the image. -->
`Image` 모델의 `imageable` 관계는 이미지의 소유 타입에 따라 `Post` 또는 `User` 인스턴스를 반환합니다.

<a name="morph-one-to-one-key-conventions"></a>
<!-- #### Key Conventions -->
#### Key Conventions

<!-- If necessary, you may specify the name of the "id" and "type" columns utilized by your polymorphic child model. If you do so, ensure that you always pass the name of the relationship as the first argument to the `morphTo` method. Typically, this value should match the method name, so you may use PHP's `__FUNCTION__` constant: -->
필요한 경우, 다형성 자식 모델이 사용하는 "id"와 "type" 컬럼명을 직접 지정할 수 있습니다. 이때 `morphTo` 메서드의 첫 번째 인수로 관계명을 반드시 전달해야 합니다. 보통 메서드명과 동일해야 하므로 PHP의 `__FUNCTION__` 상수를 사용할 수 있습니다:

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
<!-- ### One to Many (Polymorphic) -->
### One to Many (Polymorphic)

<a name="one-to-many-polymorphic-table-structure"></a>
<!-- #### Table Structure -->
#### Table Structure

<!-- A one-to-many polymorphic relation is similar to a typical one-to-many relation; however, the child model can belong to more than one type of model using a single association. For example, imagine users of your application can "comment" on posts and videos. Using polymorphic relationships, you may use a single `comments` table to contain comments for both posts and videos. First, let's examine the table structure required to build this relationship: -->
일대다 다형성 연관관계는 일반적인 일대다와 유사하지만, 자식 모델이 하나의 연관으로 둘 이상의 모델 타입에 속할 수 있습니다. 예를 들어, 게시글과 동영상 모두에 "댓글"을 달 수 있다고 가정하면, 하나의 `comments` 테이블로 양쪽 댓글을 모두 관리할 수 있습니다. 테이블 구조는 다음과 같습니다:

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
<!-- #### Model Structure -->
#### Model Structure

<!-- Next, let's examine the model definitions needed to build this relationship: -->
이 관계를 구성하기 위한 모델 정의는 다음과 같습니다:

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
<!-- #### Retrieving the Relationship -->
#### Retrieving the Relationship

<!-- Once your database table and models are defined, you may access the relationships via your model's dynamic relationship properties. For example, to access all of the comments for a post, we can use the `comments` dynamic property: -->
데이터베이스 테이블과 모델이 정의되면, 모델의 동적 연관관계 속성을 통해 관계에 접근할 수 있습니다. 예를 들어, 게시글의 모든 댓글을 가져오려면 `comments` 동적 속성을 사용합니다:

```php
use App\Models\Post;

$post = Post::find(1);

foreach ($post->comments as $comment) {
    // ...
}
```

<!-- You may also retrieve the parent of a polymorphic child model by accessing the name of the method that performs the call to `morphTo`. In this case, that is the `commentable` method on the `Comment` model. So, we will access that method as a dynamic relationship property in order to access the comment's parent model: -->
`morphTo`를 호출하는 메서드명에 접근하면 다형성 자식의 부모 모델을 가져올 수 있습니다. 이 경우 `Comment` 모델의 `commentable` 메서드이므로 동적 연관관계 속성처럼 접근합니다:

```php
use App\Models\Comment;

$comment = Comment::find(1);

$commentable = $comment->commentable;
```

<!-- The `commentable` relation on the `Comment` model will return either a `Post` or `Video` instance, depending on which type of model is the comment's parent. -->
`Comment` 모델의 `commentable` 관계는 댓글의 부모 타입에 따라 `Post` 또는 `Video` 인스턴스를 반환합니다.

<a name="polymorphic-automatically-hydrating-parent-models-on-children"></a>
<!-- #### Automatically Hydrating Parent Models on Children -->
#### Automatically Hydrating Parent Models on Children

<!-- Even when utilizing Eloquent eager loading, "N + 1" query problems can arise if you try to access the parent model from a child model while looping through the child models: -->
Eloquent의 즉시 로드를 사용하더라도, 하위 모델을 순회하면서 부모 모델에 접근하면 "N + 1" 쿼리 문제가 발생할 수 있습니다:

```php
$posts = Post::with('comments')->get();

foreach ($posts as $post) {
    foreach ($post->comments as $comment) {
        echo $comment->commentable->title;
    }
}
```

<!-- In the example above, an "N + 1" query problem has been introduced because, even though comments were eager loaded for every `Post` model, Eloquent does not automatically hydrate the parent `Post` on each child `Comment` model. -->
위 예제에서는 각 `Post` 모델의 댓글을 즉시 로드했더라도, 각 자식 `Comment` 모델에 부모 `Post`가 자동으로 할당되지 않아 "N + 1" 문제가 생깁니다.

<!-- If you would like Eloquent to automatically hydrate parent models onto their children, you may invoke the `chaperone` method when defining a `morphMany` relationship: -->
Eloquent가 자식에 부모를 자동으로 할당하도록 하려면, `morphMany` 관계 정의 시 `chaperone` 메서드를 호출하세요:

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

<!-- Or, if you would like to opt-in to automatic parent hydration at run time, you may invoke the `chaperone` model when eager loading the relationship: -->
런타임에 즉시 로드 시 `chaperone` 모델을 호출하여 자동 부모 할당을 활성화할 수도 있습니다:

```php
use App\Models\Post;

$posts = Post::with([
    'comments' => fn ($comments) => $comments->chaperone(),
])->get();
```

<a name="one-of-many-polymorphic-relations"></a>
<!-- ### One of Many (Polymorphic) -->
### One of Many (Polymorphic)

<!-- Sometimes a model may have many related models, yet you want to easily retrieve the "latest" or "oldest" related model of the relationship. For example, a `User` model may be related to many `Image` models, but you want to define a convenient way to interact with the most recent image the user has uploaded. You may accomplish this using the `morphOne` relationship type combined with the `ofMany` methods: -->
때때로 모델이 여러 관련 모델을 가질 수 있지만, "가장 최신" 또는 "가장 오래된" 관련 모델만 쉽게 가져오고 싶을 수 있습니다. 예를 들어, `User` 모델이 여러 `Image` 모델과 연관되어 있지만, 가장 최근에 업로드한 이미지 하나만 편리하게 접근하고 싶다면, `morphOne` 관계와 `ofMany` 계열 메서드를 조합할 수 있습니다:

```php
/**
 * Get the user's most recent image.
 */
public function latestImage(): MorphOne
{
    return $this->morphOne(Image::class, 'imageable')->latestOfMany();
}
```

<!-- Likewise, you may define a method to retrieve the "oldest", or first, related model of a relationship: -->
마찬가지로, "가장 오래된" 관련 모델을 가져오는 메서드도 정의할 수 있습니다:

```php
/**
 * Get the user's oldest image.
 */
public function oldestImage(): MorphOne
{
    return $this->morphOne(Image::class, 'imageable')->oldestOfMany();
}
```

<!-- By default, the `latestOfMany` and `oldestOfMany` methods will retrieve the latest or oldest related model based on the model's primary key, which must be sortable. However, sometimes you may wish to retrieve a single model from a larger relationship using a different sorting criteria. -->
기본적으로 `latestOfMany`와 `oldestOfMany` 메서드는 정렬 가능해야 하는 모델의 기본키(primary key)를 기준으로 가장 최신 또는 가장 오래된 관련 모델을 조회합니다. 하지만 때로는 다른 정렬 기준을 사용해 더 큰 연관관계에서 단일 모델을 조회하고 싶을 수 있습니다.

<!-- For example, using the `ofMany` method, you may retrieve the user's most "liked" image. The `ofMany` method accepts the sortable column as its first argument and which aggregate function (`min` or `max`) to apply when querying for the related model: -->
예를 들어 `ofMany` 메서드를 사용하면 사용자가 가장 많이 "좋아요"한 이미지를 가져올 수 있습니다. `ofMany` 메서드는 첫 번째 인수로 정렬할 컬럼을 받고, 관련 모델을 쿼리할 때 적용할 집계 함수(`min` 또는 `max`)를 받습니다:

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
> 더 복잡한 "one of many" 연관관계를 구성할 수도 있습니다. 자세한 내용은 [has one of many documentation](#advanced-has-one-of-many-relationships)를 참고하세요.

<a name="many-to-many-polymorphic-relations"></a>
<!-- ### Many to Many (Polymorphic) -->
### Many to Many (Polymorphic)

<a name="many-to-many-polymorphic-table-structure"></a>
<!-- #### Table Structure -->
#### Table Structure

<!-- Many-to-many polymorphic relations are slightly more complicated than "morph one" and "morph many" relationships. For example, a `Post` model and `Video` model could share a polymorphic relation to a `Tag` model. Using a many-to-many polymorphic relation in this situation would allow your application to have a single table of unique tags that may be associated with posts or videos. First, let's examine the table structure required to build this relationship: -->
다대다 다형성 연관관계는 "morph one"이나 "morph many"보다 약간 복잡합니다. 예를 들어, `Post`와 `Video` 모델이 `Tag` 모델과 다형성 관계를 공유할 수 있습니다. 이렇게 하면 하나의 태그 테이블로 게시글과 동영상 모두에 태그를 연결할 수 있습니다. 테이블 구조는 다음과 같습니다:

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
> 다형성 다대다 연관관계를 살펴보기 전에, 일반적인 [many-to-many relationships](#many-to-many) 문서를 먼저 읽어보시면 도움이 됩니다.

<a name="many-to-many-polymorphic-model-structure"></a>
<!-- #### Model Structure -->
#### Model Structure

<!-- Next, we're ready to define the relationships on the models. The `Post` and `Video` models will both contain a `tags` method that calls the `morphToMany` method provided by the base Eloquent model class. -->
이제 모델에서 관계를 정의할 준비가 되었습니다. `Post`와 `Video` 모델 모두 기본 Eloquent 모델 클래스의 `morphToMany` 메서드를 호출하는 `tags` 메서드를 포함합니다.

<!-- The `morphToMany` method accepts the name of the related model as well as the "relationship name". Based on the name we assigned to our intermediate table name and the keys it contains, we will refer to the relationship as "taggable": -->
`morphToMany` 메서드는 관련 모델명과 "관계명"을 인수로 받습니다. 중간 테이블 이름과 키를 기반으로, 이 관계를 "taggable"이라고 지칭합니다:

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
<!-- #### Defining the Inverse of the Relationship -->
#### Defining the Inverse of the Relationship

<!-- Next, on the `Tag` model, you should define a method for each of its possible parent models. So, in this example, we will define a `posts` method and a `videos` method. Both of these methods should return the result of the `morphedByMany` method. -->
`Tag` 모델에서는 가능한 각 부모 모델에 대한 메서드를 정의해야 합니다. 이 예시에서는 `posts`와 `videos` 메서드를 정의합니다. 두 메서드 모두 `morphedByMany`를 반환합니다.

<!-- The `morphedByMany` method accepts the name of the related model as well as the "relationship name". Based on the name we assigned to our intermediate table name and the keys it contains, we will refer to the relationship as "taggable": -->
`morphedByMany` 메서드는 관련 모델명과 "관계명"을 인수로 받습니다:

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
<!-- #### Retrieving the Relationship -->
#### Retrieving the Relationship

<!-- Once your database table and models are defined, you may access the relationships via your models. For example, to access all of the tags for a post, you may use the `tags` dynamic relationship property: -->
데이터베이스 테이블과 모델이 정의되면, 모델을 통해 관계에 접근할 수 있습니다. 예를 들어, 게시글의 모든 태그를 가져오려면 `tags` 동적 연관관계 속성을 사용합니다:

```php
use App\Models\Post;

$post = Post::find(1);

foreach ($post->tags as $tag) {
    // ...
}
```

<!-- You may retrieve the parent of a polymorphic relation from the polymorphic child model by accessing the name of the method that performs the call to `morphedByMany`. In this case, that is the `posts` or `videos` methods on the `Tag` model: -->
`morphedByMany`를 호출하는 메서드명에 접근하면 다형성 자식에서 부모 모델을 가져올 수 있습니다. 여기서는 `Tag` 모델의 `posts`나 `videos` 메서드입니다:

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
<!-- ### Custom Polymorphic Types -->
### Custom Polymorphic Types

<!-- By default, Laravel will use the fully qualified class name to store the "type" of the related model. For instance, given the one-to-many relationship example above where a `Comment` model may belong to a `Post` or a `Video` model, the default `commentable_type` would be either `App\Models\Post` or `App\Models\Video`, respectively. However, you may wish to decouple these values from your application's internal structure. -->
기본적으로 Laravel은 관련 모델의 "타입"을 저장할 때 완전한 클래스명을 사용합니다. 예를 들어, 위의 일대다 다형성 예시에서 `Comment`가 `Post` 또는 `Video`에 속할 수 있다면, `commentable_type`에는 기본적으로 `App\Models\Post` 또는 `App\Models\Video`가 저장됩니다. 하지만 이 값을 애플리케이션의 내부 구조에서 분리시키고 싶을 수 있습니다.

<!-- For example, instead of using the model names as the "type", we may use simple strings such as `post` and `video`. By doing so, the polymorphic "type" column values in our database will remain valid even if the models are renamed: -->
예를 들어, 모델명 대신 `post`, `video`와 같은 단순 문자열을 사용할 수 있습니다. 이렇게 하면 모델 이름이 변경되어도 데이터베이스의 다형성 "타입" 컬럼 값은 유효하게 유지됩니다:

```php
use Illuminate\Database\Eloquent\Relations\Relation;

Relation::enforceMorphMap([
    'post' => 'App\Models\Post',
    'video' => 'App\Models\Video',
]);
```

<!-- You may call the `enforceMorphMap` method in the `boot` method of your `App\Providers\AppServiceProvider` class or create a separate service provider if you wish. -->
`enforceMorphMap` 메서드는 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 호출하거나, 별도의 서비스 프로바이더를 생성해서 호출할 수 있습니다.

<!-- You may determine the morph alias of a given model at runtime using the model's `getMorphClass` method. Conversely, you may determine the fully-qualified class name associated with a morph alias using the `Relation::getMorphedModel` method: -->
런타임에 주어진 모델의 morph 별칭을 확인하려면 `getMorphClass` 메서드를 사용하고, morph 별칭에서 완전한 클래스명을 확인하려면 `Relation::getMorphedModel` 메서드를 사용합니다:

```php
use Illuminate\Database\Eloquent\Relations\Relation;

$alias = $post->getMorphClass();

$class = Relation::getMorphedModel($alias);
```

> [!WARNING]
> 기존 애플리케이션에 "morph map"을 추가할 경우, 데이터베이스에 아직 완전한 클래스명으로 저장되어 있는 모든 morphable `*_type` 컬럼 값을 "map" 이름으로 변환해야 합니다.

<a name="dynamic-relationships"></a>
<!-- ### Dynamic Relationships -->
### Dynamic Relationships

<!-- You may use the `resolveRelationUsing` method to define relations between Eloquent models at runtime. While not typically recommended for normal application development, this may occasionally be useful when developing Laravel packages. -->
`resolveRelationUsing` 메서드를 사용하면 런타임에 Eloquent 모델 간의 관계를 정의할 수 있습니다. 일반적인 앱 개발에서는 권장되지 않지만, Laravel 패키지 개발 시에 유용할 수 있습니다.

<!-- The `resolveRelationUsing` method accepts the desired relationship name as its first argument. The second argument passed to the method should be a closure that accepts the model instance and returns a valid Eloquent relationship definition. Typically, you should configure dynamic relationships within the boot method of a [service provider](/docs/12.x/providers): -->
`resolveRelationUsing` 메서드의 첫 번째 인수는 원하는 관계명이고, 두 번째 인수는 모델 인스턴스를 받아 유효한 Eloquent 관계 정의를 반환하는 클로저입니다. 보통 [service provider](/docs/12.x/providers)의 boot 메서드에서 동적 관계를 설정합니다:

```php
use App\Models\Order;
use App\Models\Customer;

Order::resolveRelationUsing('customer', function (Order $orderModel) {
    return $orderModel->belongsTo(Customer::class, 'customer_id');
});
```

> [!WARNING]
> 동적 관계를 정의할 때는 항상 Eloquent 관계 메서드에 명시적인 키 이름 인수를 전달해야 합니다.

<a name="querying-relations"></a>
<!-- ## Querying Relations -->
## Querying Relations

<!-- Since all Eloquent relationships are defined via methods, you may call those methods to obtain an instance of the relationship without actually executing a query to load the related models. In addition, all types of Eloquent relationships also serve as [query builders](/docs/12.x/queries), allowing you to continue to chain constraints onto the relationship query before finally executing the SQL query against your database. -->
모든 Eloquent 연관관계는 메서드를 통해 정의되므로, 관련 모델을 실제로 로드하는 쿼리를 실행하지 않고도 관계의 인스턴스를 얻을 수 있습니다. 또한, 모든 유형의 Eloquent 관계는 [query builders](/docs/12.x/queries) 역할도 하므로, SQL 쿼리를 실행하기 전에 관계 쿼리에 조건을 계속 체이닝할 수 있습니다.

<!-- For example, imagine a blog application in which a `User` model has many associated `Post` models: -->
예를 들어, `User` 모델이 여러 `Post`를 가진 블로그 앱을 상상해보세요:

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

<!-- You may query the `posts` relationship and add additional constraints to the relationship like so: -->
`posts` 관계를 쿼리하면서 추가 조건을 붙일 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

$user->posts()->where('active', 1)->get();
```

<!-- You are able to use any of the Laravel [query builder's](/docs/12.x/queries) methods on the relationship, so be sure to explore the query builder documentation to learn about all of the methods that are available to you. -->
Laravel [query builder's](/docs/12.x/queries)의 모든 메서드를 관계에 사용할 수 있으므로, 쿼리 빌더 문서를 참고해 사용 가능한 메서드를 확인하세요.

<a name="chaining-orwhere-clauses-after-relationships"></a>
<!-- #### Chaining `orWhere` Clauses After Relationships -->
#### Chaining `orWhere` Clauses After Relationships

<!-- As demonstrated in the example above, you are free to add additional constraints to relationships when querying them. However, use caution when chaining `orWhere` clauses onto a relationship, as the `orWhere` clauses will be logically grouped at the same level as the relationship constraint: -->
위 예시처럼 관계 쿼리에 추가 조건을 자유롭게 붙일 수 있지만, `orWhere` 절을 체이닝할 때는 주의가 필요합니다. `orWhere`는 관계 제약과 같은 수준에서 논리적으로 그룹핑되기 때문입니다:

```php
$user->posts()
    ->where('active', 1)
    ->orWhere('votes', '>=', 100)
    ->get();
```

<!-- The example above will generate the following SQL. As you can see, the `or` clause instructs the query to return _any_ post with greater than 100 votes. The query is no longer constrained to a specific user: -->
위 예제는 다음과 같은 SQL을 생성합니다. `or` 절 때문에 100표 이상인 _모든_ 게시글이 반환되어, 특정 사용자로 제한되지 않습니다:

```sql
select *
from posts
where user_id = ? and active = 1 or votes >= 100
```

<!-- In most situations, you should use [logical groups](/docs/12.x/queries#logical-grouping) to group the conditional checks between parentheses: -->
대부분의 경우, [logical groups](/docs/12.x/queries#logical-grouping)을 사용하여 조건 검사를 괄호로 묶어야 합니다:

```php
use Illuminate\Database\Eloquent\Builder;

$user->posts()
    ->where(function (Builder $query) {
        return $query->where('active', 1)
            ->orWhere('votes', '>=', 100);
    })
    ->get();
```

<!-- The example above will produce the following SQL. Note that the logical grouping has properly grouped the constraints and the query remains constrained to a specific user: -->
위 예제는 다음 SQL을 생성합니다. 논리적 그룹핑이 올바르게 적용되어 쿼리가 특정 사용자로 제한됩니다:

```sql
select *
from posts
where user_id = ? and (active = 1 or votes >= 100)
```

<a name="relationship-methods-vs-dynamic-properties"></a>
<!-- ### Relationship Methods vs. Dynamic Properties -->
### Relationship Methods vs. Dynamic Properties

<!-- If you do not need to add additional constraints to an Eloquent relationship query, you may access the relationship as if it were a property. For example, continuing to use our `User` and `Post` example models, we may access all of a user's posts like so: -->
Eloquent 관계 쿼리에 추가 제약을 걸 필요가 없다면, 관계를 속성처럼 접근할 수 있습니다. 예를 들어, `User`와 `Post` 모델을 사용해 사용자의 모든 게시글에 다음과 같이 접근합니다:

```php
use App\Models\User;

$user = User::find(1);

foreach ($user->posts as $post) {
    // ...
}
```

<!-- Dynamic relationship properties perform "lazy loading", meaning they will only load their relationship data when you actually access them. Because of this, developers often use [eager loading](#eager-loading) to pre-load relationships they know will be accessed after loading the model. Eager loading provides a significant reduction in SQL queries that must be executed to load a model's relations. -->
동적 연관관계 속성은 "지연 로드(lazy loading)"를 수행합니다. 즉, 실제로 접근할 때만 관계 데이터를 로드합니다. 이 때문에 개발자들은 모델 로드 후 접근할 관계를 미리 로드하는 [eager loading](#eager-loading)를 자주 사용합니다. 즉시 로드는 모델의 관계를 로드하기 위해 실행되어야 하는 SQL 쿼리를 크게 줄여줍니다.

<a name="querying-relationship-existence"></a>
<!-- ### Querying Relationship Existence -->
### Querying Relationship Existence

<!-- When retrieving model records, you may wish to limit your results based on the existence of a relationship. For example, imagine you want to retrieve all blog posts that have at least one comment. To do so, you may pass the name of the relationship to the `has` and `orHas` methods: -->
모델 레코드를 조회할 때, 관계의 존재 여부를 기반으로 결과를 제한하고 싶을 수 있습니다. 예를 들어, 댓글이 하나 이상 있는 모든 블로그 게시글을 가져오고 싶다면, 관계명을 `has`와 `orHas` 메서드에 전달합니다:

```php
use App\Models\Post;

// Retrieve all posts that have at least one comment...
$posts = Post::has('comments')->get();
```

<!-- You may also specify an operator and count value to further customize the query: -->
연산자와 개수 값을 지정하여 쿼리를 더 세밀하게 조정할 수도 있습니다:

```php
// Retrieve all posts that have three or more comments...
$posts = Post::has('comments', '>=', 3)->get();
```

<!-- Nested `has` statements may be constructed using "dot" notation. For example, you may retrieve all posts that have at least one comment that has at least one image: -->
중첩 `has` 구문은 "점" 표기법으로 작성할 수 있습니다. 예를 들어, 이미지가 있는 댓글이 하나 이상인 게시글을 가져올 수 있습니다:

```php
// Retrieve posts that have at least one comment with images...
$posts = Post::has('comments.images')->get();
```

<!-- If you need even more power, you may use the `whereHas` and `orWhereHas` methods to define additional query constraints on your `has` queries, such as inspecting the content of a comment: -->
더 세밀한 제어가 필요하면 `whereHas`와 `orWhereHas` 메서드를 사용하여 `has` 쿼리에 추가 조건을 정의할 수 있습니다:

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
> Eloquent는 현재 데이터베이스를 넘나드는 관계 존재 쿼리를 지원하지 않습니다. 관계는 동일한 데이터베이스 내에 존재해야 합니다.

<a name="many-to-many-relationship-existence-queries"></a>
<!-- #### Many to Many Relationship Existence Queries -->
#### Many to Many Relationship Existence Queries

<!-- The `whereAttachedTo` method may be used to query for models that have a many to many attachment to a model or collection of models: -->
`whereAttachedTo` 메서드를 사용하면 모델 또는 모델 컬렉션에 다대다 연결이 있는 모델을 쿼리할 수 있습니다:

```php
$users = User::whereAttachedTo($role)->get();
```

<!-- You may also provide a [collection](/docs/12.x/eloquent-collections) instance to the `whereAttachedTo` method. When doing so, Laravel will retrieve models that are attached to any of the models within the collection: -->
`whereAttachedTo`에 [collection](/docs/12.x/eloquent-collections)을 넘기면, 컬렉션 내 어떤 모델에라도 연결된 모델을 조회합니다:

```php
$tags = Tag::whereLike('name', '%laravel%')->get();

$posts = Post::whereAttachedTo($tags)->get();
```

<a name="inline-relationship-existence-queries"></a>
<!-- #### Inline Relationship Existence Queries -->
#### Inline Relationship Existence Queries

<!-- If you would like to query for a relationship's existence with a single, simple where condition attached to the relationship query, you may find it more convenient to use the `whereRelation`, `orWhereRelation`, `whereMorphRelation`, and `orWhereMorphRelation` methods. For example, we may query for all posts that have unapproved comments: -->
관계 쿼리에 단일 조건만 붙여 관계 존재를 확인하려면 `whereRelation`, `orWhereRelation`, `whereMorphRelation`, `orWhereMorphRelation` 메서드가 더 편리할 수 있습니다. 예를 들어, 승인되지 않은 댓글이 있는 게시글을 쿼리합니다:

```php
use App\Models\Post;

$posts = Post::whereRelation('comments', 'is_approved', false)->get();
```

<!-- Of course, like calls to the query builder's `where` method, you may also specify an operator: -->
물론, 쿼리 빌더의 `where` 메서드와 마찬가지로 연산자를 지정할 수도 있습니다:

```php
$posts = Post::whereRelation(
    'comments', 'created_at', '>=', now()->minus(hours: 1)
)->get();
```

<a name="querying-relationship-absence"></a>
<!-- ### Querying Relationship Absence -->
### Querying Relationship Absence

<!-- When retrieving model records, you may wish to limit your results based on the absence of a relationship. For example, imagine you want to retrieve all blog posts that **don't** have any comments. To do so, you may pass the name of the relationship to the `doesntHave` and `orDoesntHave` methods: -->
모델 레코드를 조회할 때, 관계의 부재를 기반으로 결과를 제한하고 싶을 수 있습니다. 예를 들어, 댓글이 **없는** 모든 블로그 게시글을 가져오려면, `doesntHave`와 `orDoesntHave` 메서드에 관계명을 전달합니다:

```php
use App\Models\Post;

$posts = Post::doesntHave('comments')->get();
```

<!-- If you need even more power, you may use the `whereDoesntHave` and `orWhereDoesntHave` methods to add additional query constraints to your `doesntHave` queries, such as inspecting the content of a comment: -->
더 세밀한 제어가 필요하면 `doesntHave` 쿼리에 `whereDoesntHave`와 `orWhereDoesntHave` 메서드로 추가 쿼리 조건을 붙일 수 있습니다:

```php
use Illuminate\Database\Eloquent\Builder;

$posts = Post::whereDoesntHave('comments', function (Builder $query) {
    $query->where('content', 'like', 'code%');
})->get();
```

<!-- You may use "dot" notation to execute a query against a nested relationship. For example, the following query will retrieve all posts that do not have comments as well as posts that have comments where none of the comments are from banned users: -->
"점" 표기법으로 중첩 관계에 대해서도 쿼리할 수 있습니다. 예를 들어, 다음 쿼리는 댓글이 없는 게시글과 차단된 사용자의 댓글이 없는 게시글을 가져옵니다:

```php
use Illuminate\Database\Eloquent\Builder;

$posts = Post::whereDoesntHave('comments.author', function (Builder $query) {
    $query->where('banned', 1);
})->get();
```

<a name="querying-morph-to-relationships"></a>
<!-- ### Querying Morph To Relationships -->
### Querying Morph To Relationships

<!-- To query the existence of "morph to" relationships, you may use the `whereHasMorph` and `whereDoesntHaveMorph` methods. These methods accept the name of the relationship as their first argument. Next, the methods accept the names of the related models that you wish to include in the query. Finally, you may provide a closure which customizes the relationship query: -->
"morph to" 관계의 존재를 쿼리하려면 `whereHasMorph`와 `whereDoesntHaveMorph` 메서드를 사용합니다. 이 메서드는 첫 번째 인수로 관계명, 두 번째 인수로 쿼리에 포함할 관련 모델명 배열, 그리고 선택적으로 관계 쿼리를 커스텀하는 클로저를 받습니다:

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

<!-- You may occasionally need to add query constraints based on the "type" of the related polymorphic model. The closure passed to the `whereHasMorph` method may receive a `$type` value as its second argument. This argument allows you to inspect the "type" of the query that is being built: -->
관련 다형성 모델의 "타입"에 따라 쿼리 조건을 추가해야 할 때도 있습니다. `whereHasMorph`에 전달된 클로저는 두 번째 인수로 `$type` 값을 받을 수 있으며, 이를 통해 빌드 중인 쿼리의 "타입"을 확인할 수 있습니다:

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

<!-- Sometimes you may want to query for the children of a "morph to" relationship's parent. You may accomplish this using the `whereMorphedTo` and `whereNotMorphedTo` methods, which will automatically determine the proper morph type mapping for the given model. These methods accept the name of the `morphTo` relationship as their first argument and the related parent model as their second argument: -->
때로는 "morph to" 관계의 부모 자식을 쿼리하고 싶을 수 있습니다. `whereMorphedTo`와 `whereNotMorphedTo` 메서드를 사용하면 적절한 morph 타입 매핑을 자동으로 결정합니다. 첫 번째 인수로 `morphTo` 관계명을, 두 번째 인수로 관련 부모 모델을 전달합니다:

```php
$comments = Comment::whereMorphedTo('commentable', $post)
    ->orWhereMorphedTo('commentable', $video)
    ->get();
```

<a name="querying-all-morph-to-related-models"></a>
<!-- #### Querying All Related Models -->
#### Querying All Related Models

<!-- Instead of passing an array of possible polymorphic models, you may provide `*` as a wildcard value. This will instruct Laravel to retrieve all of the possible polymorphic types from the database. Laravel will execute an additional query in order to perform this operation: -->
가능한 다형성 모델의 배열 대신 `*`를 와일드카드로 제공할 수 있습니다. 이렇게 하면 Laravel이 데이터베이스에서 가능한 모든 다형성 타입을 조회합니다. 이를 위해 추가 쿼리가 한 번 더 실행됩니다:

```php
use Illuminate\Database\Eloquent\Builder;

$comments = Comment::whereHasMorph('commentable', '*', function (Builder $query) {
    $query->where('title', 'like', 'foo%');
})->get();
```

<a name="aggregating-related-models"></a>
<!-- ## Aggregating Related Models -->
## Aggregating Related Models

<a name="counting-related-models"></a>
<!-- ### Counting Related Models -->
### Counting Related Models

<!-- Sometimes you may want to count the number of related models for a given relationship without actually loading the models. To accomplish this, you may use the `withCount` method. The `withCount` method will place a `{relation}_count` attribute on the resulting models: -->
관련 모델을 실제로 로드하지 않고 개수만 세고 싶을 때는 `withCount` 메서드를 사용합니다. `withCount`는 결과 모델에 `{relation}_count` 속성을 추가합니다:

```php
use App\Models\Post;

$posts = Post::withCount('comments')->get();

foreach ($posts as $post) {
    echo $post->comments_count;
}
```

<!-- By passing an array to the `withCount` method, you may add the "counts" for multiple relations as well as add additional constraints to the queries: -->
배열을 `withCount`에 전달하면 여러 관계의 "개수"를 추가하고, 쿼리에 추가 조건도 붙일 수 있습니다:

```php
use Illuminate\Database\Eloquent\Builder;

$posts = Post::withCount(['votes', 'comments' => function (Builder $query) {
    $query->where('content', 'like', 'code%');
}])->get();

echo $posts[0]->votes_count;
echo $posts[0]->comments_count;
```

<!-- You may also alias the relationship count result, allowing multiple counts on the same relationship: -->
관계 개수 결과에 별칭을 붙여 동일한 관계에 대해 여러 개의 카운트를 정의할 수도 있습니다:

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
<!-- #### Deferred Count Loading -->
#### Deferred Count Loading

<!-- Using the `loadCount` method, you may load a relationship count after the parent model has already been retrieved: -->
`loadCount` 메서드를 사용하면 부모 모델을 이미 가져온 뒤에도 관계 개수를 로드할 수 있습니다:

```php
$book = Book::first();

$book->loadCount('genres');
```

<!-- If you need to set additional query constraints on the count query, you may pass an array keyed by the relationships you wish to count. The array values should be closures which receive the query builder instance: -->
카운트 쿼리에 추가 조건을 설정하려면, 관계명을 키로 하고 클로저를 값으로 하는 배열을 전달합니다:

```php
$book->loadCount(['reviews' => function (Builder $query) {
    $query->where('rating', 5);
}])
```

<a name="relationship-counting-and-custom-select-statements"></a>
<!-- #### Relationship Counting and Custom Select Statements -->
#### Relationship Counting and Custom Select Statements

<!-- If you're combining `withCount` with a `select` statement, ensure that you call `withCount` after the `select` method: -->
`withCount`를 `select`와 함께 사용할 때는 반드시 `select` 메서드 뒤에 `withCount`를 호출하세요:

```php
$posts = Post::select(['title', 'body'])
    ->withCount('comments')
    ->get();
```

<a name="other-aggregate-functions"></a>
<!-- ### Other Aggregate Functions -->
### Other Aggregate Functions

<!-- In addition to the `withCount` method, Eloquent provides `withMin`, `withMax`, `withAvg`, `withSum`, and `withExists` methods. These methods will place a `{relation}_{function}_{column}` attribute on your resulting models: -->
`withCount` 외에도 Eloquent는 `withMin`, `withMax`, `withAvg`, `withSum`, `withExists` 메서드를 제공합니다. 이 메서드들은 결과 모델에 `{relation}_{function}_{column}` 속성을 추가합니다:

```php
use App\Models\Post;

$posts = Post::withSum('comments', 'votes')->get();

foreach ($posts as $post) {
    echo $post->comments_sum_votes;
}
```

<!-- If you wish to access the result of the aggregate function using another name, you may specify your own alias: -->
집계 함수 결과에 별칭을 사용하고 싶다면 다음과 같이 지정합니다:

```php
$posts = Post::withSum('comments as total_comments', 'votes')->get();

foreach ($posts as $post) {
    echo $post->total_comments;
}
```

<!-- Like the `loadCount` method, deferred versions of these methods are also available. These additional aggregate operations may be performed on Eloquent models that have already been retrieved: -->
`loadCount`와 마찬가지로 지연 버전도 사용 가능합니다. 이미 조회된 Eloquent 모델에 대해 추가 집계 연산을 수행할 수 있습니다:

```php
$post = Post::first();

$post->loadSum('comments', 'votes');
```

<!-- If you're combining these aggregate methods with a `select` statement, ensure that you call the aggregate methods after the `select` method: -->
집계 메서드를 `select`와 함께 사용할 때는 `select` 뒤에 호출하세요:

```php
$posts = Post::select(['title', 'body'])
    ->withExists('comments')
    ->get();
```

<a name="counting-related-models-on-morph-to-relationships"></a>
<!-- ### Counting Related Models on Morph To Relationships -->
### Counting Related Models on Morph To Relationships

<!-- If you would like to eager load a "morph to" relationship, as well as related model counts for the various entities that may be returned by that relationship, you may utilize the `with` method in combination with the `morphTo` relationship's `morphWithCount` method. -->
"morph to" 관계를 즉시 로드하면서, 해당 관계가 반환할 수 있는 다양한 엔티티의 관련 모델 개수도 함께 로드하려면 `with` 메서드와 `morphTo` 관계의 `morphWithCount` 메서드를 조합합니다.

<!-- In this example, let's assume that `Photo` and `Post` models may create `ActivityFeed` models. We will assume the `ActivityFeed` model defines a "morph to" relationship named `parentable` that allows us to retrieve the parent `Photo` or `Post` model for a given `ActivityFeed` instance. Additionally, let's assume that `Photo` models "have many" `Tag` models and `Post` models "have many" `Comment` models. -->
이 예제에서는 `Photo`와 `Post` 모델이 `ActivityFeed` 모델을 생성할 수 있다고 가정합니다. `ActivityFeed` 모델에는 `parentable`이라는 "morph to" 관계가 정의되어 있으며, 각 `ActivityFeed` 레코드의 부모 `Photo` 또는 `Post` 모델을 가져올 수 있습니다. 또한 `Photo` 모델은 여러 `Tag`를, `Post` 모델은 여러 `Comment`를 가집니다.

<!-- Now, let's imagine we want to retrieve `ActivityFeed` instances and eager load the `parentable` parent models for each `ActivityFeed` instance. In addition, we want to retrieve the number of tags that are associated with each parent photo and the number of comments that are associated with each parent post: -->
`ActivityFeed` 인스턴스를 조회하면서 각 `ActivityFeed` 인스턴스의 `parentable` 부모 모델을 즉시 로드하고, 각 부모 사진의 태그 수와 게시글의 댓글 수도 함께 가져오려면:

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
<!-- #### Deferred Count Loading -->
#### Deferred Count Loading

<!-- Let's assume we have already retrieved a set of `ActivityFeed` models and now we would like to load the nested relationship counts for the various `parentable` models associated with the activity feeds. You may use the `loadMorphCount` method to accomplish this: -->
이미 `ActivityFeed` 모델 집합을 조회한 뒤, 관련 `parentable` 모델들의 중첩된 관계 카운트를 로드하려면 `loadMorphCount` 메서드를 사용합니다:

```php
$activities = ActivityFeed::with('parentable')->get();

$activities->loadMorphCount('parentable', [
    Photo::class => ['tags'],
    Post::class => ['comments'],
]);
```

<a name="eager-loading"></a>
<!-- ## Eager Loading -->
## Eager Loading

<!-- When accessing Eloquent relationships as properties, the related models are "lazy loaded". This means the relationship data is not actually loaded until you first access the property. However, Eloquent can "eager load" relationships at the time you query the parent model. Eager loading alleviates the "N + 1" query problem. To illustrate the N + 1 query problem, consider a `Book` model that "belongs to" to an `Author` model: -->
Eloquent 관계를 속성으로 접근하면, 관련 모델은 "지연 로드(lazy load)"됩니다. 즉, 속성에 처음 접근할 때까지 관계 데이터가 실제로 로드되지 않습니다. 하지만 Eloquent에서는 부모 모델 쿼리 시점에 관계를 "즉시 로드(eager load)"할 수 있습니다. 즉시 로드는 "N + 1" 쿼리 문제를 해결합니다. N + 1 쿼리 문제를 설명하기 위해, `Author`에 "속하는(belongs to)" `Book` 모델을 생각해봅시다:

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

<!-- Now, let's retrieve all books and their authors: -->
이제 모든 책과 저자를 조회해봅니다:

```php
use App\Models\Book;

$books = Book::all();

foreach ($books as $book) {
    echo $book->author->name;
}
```

<!-- This loop will execute one query to retrieve all of the books within the database table, then another query for each book in order to retrieve the book's author. So, if we have 25 books, the code above would run 26 queries: one for the original book, and 25 additional queries to retrieve the author of each book. -->
이 루프는 데이터베이스에서 모든 책을 가져오기 위해 쿼리 1개, 그리고 각 책마다 저자를 가져오기 위해 추가 쿼리를 실행합니다. 책이 25권이라면 총 26개의 쿼리가 실행됩니다.

<!-- Thankfully, we can use eager loading to reduce this operation to just two queries. When building a query, you may specify which relationships should be eager loaded using the `with` method: -->
다행히 즉시 로드를 사용하면 이 작업을 단 2개의 쿼리로 줄일 수 있습니다. 쿼리를 빌드할 때 `with` 메서드로 즉시 로드할 관계를 지정합니다:

```php
$books = Book::with('author')->get();

foreach ($books as $book) {
    echo $book->author->name;
}
```

<!-- For this operation, only two queries will be executed - one query to retrieve all of the books and one query to retrieve all of the authors for all of the books: -->
이 경우 쿼리는 2개만 실행됩니다 - 하나는 모든 책 조회, 하나는 모든 책의 저자 조회:

```sql
select * from books

select * from authors where id in (1, 2, 3, 4, 5, ...)
```

<a name="eager-loading-multiple-relationships"></a>
<!-- #### Eager Loading Multiple Relationships -->
#### Eager Loading Multiple Relationships

<!-- Sometimes you may need to eager load several different relationships. To do so, just pass an array of relationships to the `with` method: -->
여러 개의 다른 관계를 즉시 로드해야 할 때는 `with` 메서드에 관계 배열을 전달하면 됩니다:

```php
$books = Book::with(['author', 'publisher'])->get();
```

<a name="nested-eager-loading"></a>
<!-- #### Nested Eager Loading -->
#### Nested Eager Loading

<!-- To eager load a relationship's relationships, you may use "dot" syntax. For example, let's eager load all of the book's authors and all of the author's personal contacts: -->
관계의 관계를 즉시 로드하려면 "점" 표기법을 사용합니다. 예를 들어, 모든 책의 저자와 저자의 연락처 정보를 즉시 로드합니다:

```php
$books = Book::with('author.contacts')->get();
```

<!-- Alternatively, you may specify nested eager loaded relationships by providing a nested array to the `with` method, which can be convenient when eager loading multiple nested relationships: -->
또는 `with` 메서드에 중첩 배열을 전달하여 여러 중첩 관계를 즉시 로드할 수도 있습니다:

```php
$books = Book::with([
    'author' => [
        'contacts',
        'publisher',
    ],
])->get();
```

<a name="nested-eager-loading-morphto-relationships"></a>
<!-- #### Nested Eager Loading `morphTo` Relationships -->
#### Nested Eager Loading `morphTo` Relationships

<!-- If you would like to eager load a `morphTo` relationship, as well as nested relationships on the various entities that may be returned by that relationship, you may use the `with` method in combination with the `morphTo` relationship's `morphWith` method. To help illustrate this method, let's consider the following model: -->
`morphTo` 관계를 즉시 로드하면서, 해당 관계가 반환할 수 있는 다양한 엔티티의 중첩 관계도 함께 로드하려면 `with` 메서드와 `morphTo` 관계의 `morphWith` 메서드를 조합합니다. 다음 모델을 참고하세요:

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

<!-- In this example, let's assume `Event`, `Photo`, and `Post` models may create `ActivityFeed` models. Additionally, let's assume that `Event` models belong to a `Calendar` model, `Photo` models are associated with `Tag` models, and `Post` models belong to an `Author` model. -->
이 예제에서 `Event`, `Photo`, `Post` 모델이 `ActivityFeed`를 생성할 수 있다고 가정합니다. `Event` 모델은 `Calendar`에 속하고, `Photo`는 `Tag`와 연관되며, `Post`는 `Author`에 속합니다.

<!-- Using these model definitions and relationships, we may retrieve `ActivityFeed` model instances and eager load all `parentable` models and their respective nested relationships: -->
이 모델 정의와 관계를 사용하여, `ActivityFeed` 모델 인스턴스를 조회하면서 모든 `parentable` 모델과 각각의 중첩 관계를 즉시 로드합니다:

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
<!-- #### Eager Loading Specific Columns -->
#### Eager Loading Specific Columns

<!-- You may not always need every column from the relationships you are retrieving. For this reason, Eloquent allows you to specify which columns of the relationship you would like to retrieve: -->
관계에서 모든 컬럼이 필요하지 않을 때는, 가져올 컬럼을 지정할 수 있습니다:

```php
$books = Book::with('author:id,name,book_id')->get();
```

> [!WARNING]
> 이 기능을 사용할 때는 가져올 컬럼 목록에 반드시 `id` 컬럼과 관련 외래키 컬럼을 포함해야 합니다.

<a name="eager-loading-by-default"></a>
<!-- #### Eager Loading by Default -->
#### Eager Loading by Default

<!-- Sometimes you might want to always load some relationships when retrieving a model. To accomplish this, you may define a `$with` property on the model: -->
모델 조회 시 항상 특정 관계를 로드하고 싶다면, 모델에 `$with` 속성을 정의합니다:

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

<!-- If you would like to remove an item from the `$with` property for a single query, you may use the `without` method: -->
특정 쿼리에서 `$with`의 항목을 제거하려면 `without` 메서드를 사용합니다:

```php
$books = Book::without('author')->get();
```

<!-- If you would like to override all items within the `$with` property for a single query, you may use the `withOnly` method: -->
특정 쿼리에서 `$with`의 모든 항목을 재정의하려면 `withOnly` 메서드를 사용합니다:

```php
$books = Book::withOnly('genre')->get();
```

<a name="constraining-eager-loads"></a>
<!-- ### Constraining Eager Loads -->
### Constraining Eager Loads

<!-- Sometimes you may wish to eager load a relationship but also specify additional query conditions for the eager loading query. You can accomplish this by passing an array of relationships to the `with` method where the array key is a relationship name and the array value is a closure that adds additional constraints to the eager loading query: -->
관계를 즉시 로드하면서 추가 쿼리 조건을 지정하고 싶을 때는, `with` 메서드에 관계명을 키로, 클로저를 값으로 하는 배열을 전달합니다:

```php
use App\Models\User;

$users = User::with(['posts' => function ($query) {
    $query->where('title', 'like', '%code%');
}])->get();
```

<!-- In this example, Eloquent will only eager load posts where the post's `title` column contains the word `code`. You may call other [query builder](/docs/12.x/queries) methods to further customize the eager loading operation: -->
이 예제에서 Eloquent는 게시글의 `title` 컬럼에 `code`가 포함된 게시글만 즉시 로드합니다. 다른 [query builder](/docs/12.x/queries) 메서드도 호출하여 즉시 로드를 더 세밀하게 조정할 수 있습니다:

```php
$users = User::with(['posts' => function ($query) {
    $query->orderBy('created_at', 'desc');
}])->get();
```

<a name="constraining-eager-loading-of-morph-to-relationships"></a>
<!-- #### Constraining Eager Loading of `morphTo` Relationships -->
#### Constraining Eager Loading of `morphTo` Relationships

<!-- If you are eager loading a `morphTo` relationship, Eloquent will run multiple queries to fetch each type of related model. You may add additional constraints to each of these queries using the `MorphTo` relation's `constrain` method: -->
`morphTo` 관계를 즉시 로드할 때, Eloquent는 각 관련 모델 타입마다 별도의 쿼리를 실행합니다. `MorphTo` 관계의 `constrain` 메서드로 각 쿼리에 조건을 추가할 수 있습니다:

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

<!-- In this example, Eloquent will only eager load posts that have not been hidden and videos that have a `type` value of "educational". -->
이 예제에서 Eloquent는 숨겨지지 않은 게시글과 `type` 값이 "educational"인 동영상만 즉시 로드합니다.

<a name="constraining-eager-loads-with-relationship-existence"></a>
<!-- #### Constraining Eager Loads With Relationship Existence -->
#### Constraining Eager Loads With Relationship Existence

<!-- You may sometimes find yourself needing to check for the existence of a relationship while simultaneously loading the relationship based on the same conditions. For example, you may wish to only retrieve `User` models that have child `Post` models matching a given query condition while also eager loading the matching posts. You may accomplish this using the `withWhereHas` method: -->
관계의 존재를 확인하면서 동시에 같은 조건으로 관계를 즉시 로드해야 할 때가 있습니다. 예를 들어, 특정 쿼리 조건에 맞는 자식 `Post`를 가진 `User` 모델만 가져오면서 일치하는 게시글도 즉시 로드하려면 `withWhereHas` 메서드를 사용합니다:

```php
use App\Models\User;

$users = User::withWhereHas('posts', function ($query) {
    $query->where('featured', true);
})->get();
```

<a name="lazy-eager-loading"></a>
<!-- ### Lazy Eager Loading -->
### Lazy Eager Loading

<!-- Sometimes you may need to eager load a relationship after the parent model has already been retrieved. For example, this may be useful if you need to dynamically decide whether to load related models: -->
부모 모델이 이미 조회된 뒤에 관계를 즉시 로드해야 할 때가 있습니다. 예를 들어, 관련 모델의 로드 여부를 동적으로 결정해야 하는 경우에 유용합니다:

```php
use App\Models\Book;

$books = Book::all();

if ($condition) {
    $books->load('author', 'publisher');
}
```

<!-- If you need to set additional query constraints on the eager loading query, you may pass an array keyed by the relationships you wish to load. The array values should be closure instances which receive the query instance: -->
즉시 로드 쿼리에 추가 조건을 설정하려면, 관계명을 키로 하는 배열에 쿼리 인스턴스를 받는 클로저를 값으로 전달합니다:

```php
$author->load(['books' => function ($query) {
    $query->orderBy('published_date', 'asc');
}]);
```

<!-- To load a relationship only when it has not already been loaded, use the `loadMissing` method: -->
아직 로드되지 않은 관계만 로드하려면 `loadMissing` 메서드를 사용합니다:

```php
$book->loadMissing('author');
```

<a name="nested-lazy-eager-loading-morphto"></a>
<!-- #### Nested Lazy Eager Loading and `morphTo` -->
#### Nested Lazy Eager Loading and `morphTo`

<!-- If you would like to eager load a `morphTo` relationship, as well as nested relationships on the various entities that may be returned by that relationship, you may use the `loadMorph` method. -->
`morphTo` 관계와 해당 관계가 반환할 수 있는 다양한 엔티티의 중첩 관계를 즉시 로드하려면 `loadMorph` 메서드를 사용합니다.

<!-- This method accepts the name of the `morphTo` relationship as its first argument, and an array of model / relationship pairs as its second argument. To help illustrate this method, let's consider the following model: -->
이 메서드는 첫 번째 인수로 `morphTo` 관계명을, 두 번째 인수로 모델/관계 쌍의 배열을 받습니다. 다음 모델을 참고하세요:

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

<!-- In this example, let's assume `Event`, `Photo`, and `Post` models may create `ActivityFeed` models. Additionally, let's assume that `Event` models belong to a `Calendar` model, `Photo` models are associated with `Tag` models, and `Post` models belong to an `Author` model. -->
이 예제에서 `Event`, `Photo`, `Post` 모델이 `ActivityFeed`를 생성할 수 있다고 가정합니다. `Event`는 `Calendar`에, `Photo`는 `Tag`에, `Post`는 `Author`에 속합니다.

<!-- Using these model definitions and relationships, we may retrieve `ActivityFeed` model instances and eager load all `parentable` models and their respective nested relationships: -->
이 모델 정의와 관계를 사용하여 `ActivityFeed` 인스턴스를 조회한 뒤, 모든 `parentable` 모델과 각각의 중첩 관계를 즉시 로드합니다:

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
<!-- ### Automatic Eager Loading -->
### Automatic Eager Loading

> [!WARNING]
> 이 기능은 현재 커뮤니티 피드백을 수집하기 위해 베타 상태입니다. 이 기능의 동작과 기능은 패치 릴리스에서도 변경될 수 있습니다.

<!-- In many cases, Laravel can automatically eager load the relationships you access. To enable automatic eager loading, you should invoke the `Model::automaticallyEagerLoadRelationships` method within the `boot` method of your application's `AppServiceProvider`: -->
많은 경우 Laravel이 접근하는 관계를 자동으로 즉시 로드할 수 있습니다. 자동 즉시 로드를 활성화하려면, 앱의 `AppServiceProvider`의 `boot` 메서드에서 `Model::automaticallyEagerLoadRelationships` 메서드를 호출합니다:

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

<!-- When this feature is enabled, Laravel will attempt to automatically load any relationships you access that have not been previously loaded. For example, consider the following scenario: -->
이 기능이 활성화되면, Laravel은 이전에 로드되지 않은 관계에 접근할 때 자동으로 로드를 시도합니다. 예를 들어:

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

<!-- Typically, the code above would execute a query for each user in order to retrieve their posts, as well as a query for each post to retrieve its comments. However, when the `automaticallyEagerLoadRelationships` feature has been enabled, Laravel will automatically [lazy eager load](#lazy-eager-loading) the posts for all users in the user collection when you attempt to access the posts on any of the retrieved users. Likewise, when you attempt to access the comments for any retrieved post, all comments will be lazy eager loaded for all posts that were originally retrieved. -->
일반적으로 위 코드는 각 사용자의 게시글 조회를 위해, 그리고 각 게시글의 댓글 조회를 위해 개별 쿼리를 실행합니다. 하지만 `automaticallyEagerLoadRelationships` 기능이 활성화되면, 사용자 컬렉션 중 어느 사용자의 게시글에 접근할 때 Laravel이 자동으로 모든 사용자의 게시글을 [lazy eager load](#lazy-eager-loading)합니다. 마찬가지로, 어느 게시글의 댓글에 접근하면 원래 조회한 모든 게시글의 댓글이 지연 즉시 로드됩니다.

<!-- If you do not want to globally enable automatic eager loading, you can still enable this feature for a single Eloquent collection instance by invoking the `withRelationshipAutoloading` method on the collection: -->
전역으로 자동 즉시 로드를 활성화하지 않으려면, 단일 Eloquent 컬렉션 인스턴스에서 `withRelationshipAutoloading` 메서드를 호출하여 활성화할 수 있습니다:

```php
$users = User::where('vip', true)->get();

return $users->withRelationshipAutoloading();
```

<a name="preventing-lazy-loading"></a>
<!-- ### Preventing Lazy Loading -->
### Preventing Lazy Loading

<!-- As previously discussed, eager loading relationships can often provide significant performance benefits to your application. Therefore, if you would like, you may instruct Laravel to always prevent the lazy loading of relationships. To accomplish this, you may invoke the `preventLazyLoading` method offered by the base Eloquent model class. Typically, you should call this method within the `boot` method of your application's `AppServiceProvider` class. -->
앞서 설명한 것처럼, 관계를 즉시 로드하면 애플리케이션에 상당한 성능 이점을 제공할 수 있습니다. 원한다면 Laravel에 관계의 지연 로드를 항상 방지하도록 지시할 수 있습니다. 이를 위해 Eloquent 모델 기본 클래스의 `preventLazyLoading` 메서드를 호출합니다. 보통 앱의 `AppServiceProvider` 클래스의 `boot` 메서드에서 호출합니다.

<!-- The `preventLazyLoading` method accepts an optional boolean argument that indicates if lazy loading should be prevented. For example, you may wish to only disable lazy loading in non-production environments so that your production environment will continue to function normally even if a lazy loaded relationship is accidentally present in production code: -->
`preventLazyLoading` 메서드는 지연 로드 방지 여부를 나타내는 선택적 boolean 인수를 받습니다. 예를 들어, 프로덕션이 아닌 환경에서만 지연 로드를 비활성화하여, 프로덕션 환경에서는 정상적으로 동작하면서도 실수로 지연 로드된 관계가 프로덕션 코드에 있어도 문제없게 할 수 있습니다:

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

<!-- After preventing lazy loading, Eloquent will throw a `Illuminate\Database\LazyLoadingViolationException` exception when your application attempts to lazy load any Eloquent relationship. -->
지연 로드를 방지한 후, Eloquent 관계의 지연 로드를 시도하면 `Illuminate\Database\LazyLoadingViolationException` 예외가 발생합니다.

<!-- You may customize the behavior of lazy loading violations using the `handleLazyLoadingViolationsUsing` method. For example, using this method, you may instruct lazy loading violations to only be logged instead of interrupting the application's execution with exceptions: -->
`handleLazyLoadingViolationsUsing` 메서드로 지연 로드 위반 시 동작을 커스텀할 수 있습니다. 예를 들어, 예외 대신 로그만 기록하도록 설정할 수 있습니다:

```php
Model::handleLazyLoadingViolationUsing(function (Model $model, string $relation) {
    $class = $model::class;

    info("Attempted to lazy load [{$relation}] on model [{$class}].");
});
```

<a name="inserting-and-updating-related-models"></a>
<!-- ## Inserting and Updating Related Models -->
## Inserting and Updating Related Models

<a name="the-save-method"></a>
<!-- ### The `save` Method -->
### The `save` Method

<!-- Eloquent provides convenient methods for adding new models to relationships. For example, perhaps you need to add a new comment to a post. Instead of manually setting the `post_id` attribute on the `Comment` model you may insert the comment using the relationship's `save` method: -->
Eloquent는 관계에 새 모델을 추가하는 편리한 메서드를 제공합니다. 예를 들어, 게시글에 새 댓글을 추가할 때, `Comment` 모델의 `post_id` 속성을 직접 설정하는 대신 관계의 `save` 메서드를 사용할 수 있습니다:

```php
use App\Models\Comment;
use App\Models\Post;

$comment = new Comment(['message' => 'A new comment.']);

$post = Post::find(1);

$post->comments()->save($comment);
```

<!-- Note that we did not access the `comments` relationship as a dynamic property. Instead, we called the `comments` method to obtain an instance of the relationship. The `save` method will automatically add the appropriate `post_id` value to the new `Comment` model. -->
`comments` 관계에 동적 속성이 아닌 메서드로 접근한 점에 주의하세요. 대신 관계 인스턴스를 얻기 위해 `comments` 메서드를 호출했습니다. `save` 메서드는 새 `Comment` 모델에 적절한 `post_id` 값을 자동으로 추가합니다.

<!-- If you need to save multiple related models, you may use the `saveMany` method: -->
여러 관련 모델을 저장하려면 `saveMany` 메서드를 사용합니다:

```php
$post = Post::find(1);

$post->comments()->saveMany([
    new Comment(['message' => 'A new comment.']),
    new Comment(['message' => 'Another new comment.']),
]);
```

<!-- The `save` and `saveMany` methods will persist the given model instances, but will not add the newly persisted models to any in-memory relationships that are already loaded onto the parent model. If you plan on accessing the relationship after using the `save` or `saveMany` methods, you may wish to use the `refresh` method to reload the model and its relationships: -->
`save`와 `saveMany` 메서드는 주어진 모델 인스턴스를 영속화하지만, 부모 모델에 이미 로드된 인메모리 관계에 새로 저장된 모델을 추가하지는 않습니다. `save`나 `saveMany` 사용 후 관계에 접근할 계획이라면 `refresh` 메서드를 사용하여 모델과 관계를 다시 로드하세요:

```php
$post->comments()->save($comment);

$post->refresh();

// All comments, including the newly saved comment...
$post->comments;
```

<a name="the-push-method"></a>
<!-- #### Recursively Saving Models and Relationships -->
#### Recursively Saving Models and Relationships

<!-- If you would like to `save` your model and all of its associated relationships, you may use the `push` method. In this example, the `Post` model will be saved as well as its comments and the comment's authors: -->
모델과 모든 연관 관계를 함께 `save`하려면 `push` 메서드를 사용합니다. 이 예제에서 `Post` 모델과 그 댓글, 댓글의 작성자가 모두 저장됩니다:

```php
$post = Post::find(1);

$post->comments[0]->message = 'Message';
$post->comments[0]->author->name = 'Author Name';

$post->push();
```

<!-- The `pushQuietly` method may be used to save a model and its associated relationships without raising any events: -->
이벤트를 발생시키지 않고 모델과 관계를 저장하려면 `pushQuietly` 메서드를 사용합니다:

```php
$post->pushQuietly();
```

<a name="the-create-method"></a>
<!-- ### The `create` Method -->
### The `create` Method

<!-- In addition to the `save` and `saveMany` methods, you may also use the `create` method, which accepts an array of attributes, creates a model, and inserts it into the database. The difference between `save` and `create` is that `save` accepts a full Eloquent model instance while `create` accepts a plain PHP `array`. The newly created model will be returned by the `create` method: -->
`save`와 `saveMany` 외에도 `create` 메서드를 사용할 수 있습니다. 이 메서드는 속성 배열을 받아 모델을 생성하고 데이터베이스에 삽입합니다. `save`와 `create`의 차이점은 `save`가 전체 Eloquent 모델 인스턴스를 받는 반면, `create`는 일반 PHP `array`를 받는다는 것입니다. `create` 메서드는 새로 생성된 모델을 반환합니다:

```php
use App\Models\Post;

$post = Post::find(1);

$comment = $post->comments()->create([
    'message' => 'A new comment.',
]);
```

<!-- You may use the `createMany` method to create multiple related models: -->
`createMany` 메서드로 여러 관련 모델을 생성할 수 있습니다:

```php
$post = Post::find(1);

$post->comments()->createMany([
    ['message' => 'A new comment.'],
    ['message' => 'Another new comment.'],
]);
```

<!-- The `createQuietly` and `createManyQuietly` methods may be used to create a model(s) without dispatching any events: -->
`createQuietly`와 `createManyQuietly` 메서드는 이벤트를 발생시키지 않고 모델을 생성합니다:

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

<!-- You may also use the `findOrNew`, `firstOrNew`, `firstOrCreate`, and `updateOrCreate` methods to [create and update models on relationships](/docs/12.x/eloquent#upserts). -->
`findOrNew`, `firstOrNew`, `firstOrCreate`, `updateOrCreate` 메서드를 사용하여 [create and update models on relationships](/docs/12.x/eloquent#upserts)할 수도 있습니다.

> [!NOTE]
> `create` 메서드를 사용하기 전에 [mass assignment](/docs/12.x/eloquent#mass-assignment) 문서를 반드시 확인하세요.

<a name="updating-belongs-to-relationships"></a>
<!-- ### Belongs To Relationships -->
### Belongs To Relationships

<!-- If you would like to assign a child model to a new parent model, you may use the `associate` method. In this example, the `User` model defines a `belongsTo` relationship to the `Account` model. This `associate` method will set the foreign key on the child model: -->
자식 모델을 새 부모 모델에 할당하려면 `associate` 메서드를 사용합니다. 이 예제에서 `User` 모델은 `Account` 모델에 대해 `belongsTo` 관계를 정의합니다. `associate` 메서드는 자식 모델의 외래키를 설정합니다:

```php
use App\Models\Account;

$account = Account::find(10);

$user->account()->associate($account);

$user->save();
```

<!-- To remove a parent model from a child model, you may use the `dissociate` method. This method will set the relationship's foreign key to `null`: -->
자식 모델에서 부모를 제거하려면 `dissociate` 메서드를 사용합니다. 이 메서드는 관계의 외래키를 `null`로 설정합니다:

```php
$user->account()->dissociate();

$user->save();
```

<a name="updating-many-to-many-relationships"></a>
<!-- ### Many to Many Relationships -->
### Many to Many Relationships

<a name="attaching-detaching"></a>
<!-- #### Attaching / Detaching -->
#### Attaching / Detaching

<!-- Eloquent also provides methods to make working with many-to-many relationships more convenient. For example, let's imagine a user can have many roles and a role can have many users. You may use the `attach` method to attach a role to a user by inserting a record in the relationship's intermediate table: -->
Eloquent는 다대다 연관관계를 더 편리하게 다루기 위한 메서드도 제공합니다. 예를 들어, 사용자가 여러 역할을 가지고, 역할이 여러 사용자를 가질 수 있다고 합시다. `attach` 메서드로 관계의 중간 테이블에 레코드를 삽입하여 역할을 사용자에게 연결할 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

$user->roles()->attach($roleId);
```

<!-- When attaching a relationship to a model, you may also pass an array of additional data to be inserted into the intermediate table: -->
관계를 연결할 때, 중간 테이블에 삽입할 추가 데이터를 배열로 전달할 수도 있습니다:

```php
$user->roles()->attach($roleId, ['expires' => $expires]);
```

<!-- Sometimes it may be necessary to remove a role from a user. To remove a many-to-many relationship record, use the `detach` method. The `detach` method will delete the appropriate record out of the intermediate table; however, both models will remain in the database: -->
사용자에게서 역할을 제거해야 할 때는 `detach` 메서드를 사용합니다. `detach`는 중간 테이블에서 해당 레코드를 삭제하지만, 양쪽 모델은 데이터베이스에 남아 있습니다:

```php
// Detach a single role from the user...
$user->roles()->detach($roleId);

// Detach all roles from the user...
$user->roles()->detach();
```

<!-- For convenience, `attach` and `detach` also accept arrays of IDs as input: -->
편의를 위해 `attach`와 `detach`는 ID 배열도 입력으로 받습니다:

```php
$user = User::find(1);

$user->roles()->detach([1, 2, 3]);

$user->roles()->attach([
    1 => ['expires' => $expires],
    2 => ['expires' => $expires],
]);
```

<a name="syncing-associations"></a>
<!-- #### Syncing Associations -->
#### Syncing Associations

<!-- You may also use the `sync` method to construct many-to-many associations. The `sync` method accepts an array of IDs to place on the intermediate table. Any IDs that are not in the given array will be removed from the intermediate table. So, after this operation is complete, only the IDs in the given array will exist in the intermediate table: -->
`sync` 메서드를 사용하여 다대다 연결을 구성할 수도 있습니다. `sync` 메서드는 중간 테이블에 배치할 ID 배열을 받습니다. 주어진 배열에 없는 ID는 중간 테이블에서 제거됩니다. 따라서 이 작업이 완료되면 주어진 배열의 ID만 중간 테이블에 존재합니다:

```php
$user->roles()->sync([1, 2, 3]);
```

<!-- You may also pass additional intermediate table values with the IDs: -->
ID와 함께 추가 중간 테이블 값을 전달할 수도 있습니다:

```php
$user->roles()->sync([1 => ['expires' => true], 2, 3]);
```

<!-- If you would like to insert the same intermediate table values with each of the synced model IDs, you may use the `syncWithPivotValues` method: -->
동기화된 모든 모델 ID에 동일한 중간 테이블 값을 삽입하려면 `syncWithPivotValues` 메서드를 사용합니다:

```php
$user->roles()->syncWithPivotValues([1, 2, 3], ['active' => true]);
```

<!-- If you do not want to detach existing IDs that are missing from the given array, you may use the `syncWithoutDetaching` method: -->
주어진 배열에 없는 기존 ID를 분리하지 않으려면 `syncWithoutDetaching` 메서드를 사용합니다:

```php
$user->roles()->syncWithoutDetaching([1, 2, 3]);
```

<a name="toggling-associations"></a>
<!-- #### Toggling Associations -->
#### Toggling Associations

<!-- The many-to-many relationship also provides a `toggle` method which "toggles" the attachment status of the given related model IDs. If the given ID is currently attached, it will be detached. Likewise, if it is currently detached, it will be attached: -->
다대다 관계는 주어진 관련 모델 ID의 연결 상태를 "토글"하는 `toggle` 메서드도 제공합니다. 현재 연결되어 있으면 해제하고, 해제되어 있으면 연결합니다:

```php
$user->roles()->toggle([1, 2, 3]);
```

<!-- You may also pass additional intermediate table values with the IDs: -->
ID와 함께 추가 중간 테이블 값을 전달할 수도 있습니다:

```php
$user->roles()->toggle([
    1 => ['expires' => true],
    2 => ['expires' => true],
]);
```

<a name="updating-a-record-on-the-intermediate-table"></a>
<!-- #### Updating a Record on the Intermediate Table -->
#### Updating a Record on the Intermediate Table

<!-- If you need to update an existing row in your relationship's intermediate table, you may use the `updateExistingPivot` method. This method accepts the intermediate record foreign key and an array of attributes to update: -->
관계의 중간 테이블의 기존 행을 수정하려면 `updateExistingPivot` 메서드를 사용합니다. 이 메서드는 중간 레코드의 외래키와 업데이트할 속성 배열을 받습니다:

```php
$user = User::find(1);

$user->roles()->updateExistingPivot($roleId, [
    'active' => false,
]);
```

<a name="touching-parent-timestamps"></a>
<!-- ## Touching Parent Timestamps -->
## Touching Parent Timestamps

<!-- When a model defines a `belongsTo` or `belongsToMany` relationship to another model, such as a `Comment` which belongs to a `Post`, it is sometimes helpful to update the parent's timestamp when the child model is updated. -->
모델이 `Comment`가 `Post`에 속하는 것처럼 `belongsTo` 또는 `belongsToMany` 관계를 정의할 때, 자식 모델이 업데이트될 때 부모의 타임스탬프를 갱신하면 유용한 경우가 있습니다.

<!-- For example, when a `Comment` model is updated, you may want to automatically "touch" the `updated_at` timestamp of the owning `Post` so that it is set to the current date and time. To accomplish this, you may add a `touches` property to your child model containing the names of the relationships that should have their `updated_at` timestamps updated when the child model is updated: -->
예를 들어, `Comment` 모델이 업데이트될 때 소유 `Post`의 `updated_at` 타임스탬프를 자동으로 "터치"하여 현재 날짜와 시간으로 설정하고 싶을 수 있습니다. 이를 위해 자식 모델에 `touches` 속성을 추가하고, 자식 모델이 업데이트될 때 `updated_at` 타임스탬프를 갱신할 관계명을 지정합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Comment extends Model
{
    /**
     * All of the relationships to be touched.
     *
     * @var array
     */
    protected $touches = ['post'];

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
> 부모 모델의 타임스탬프는 자식 모델이 Eloquent의 `save` 메서드를 사용하여 업데이트될 때만 갱신됩니다.
