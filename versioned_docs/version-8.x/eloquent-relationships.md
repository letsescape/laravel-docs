<!-- # Eloquent: Relationships -->
# Eloquent: Relationships

- [Introduction](#introduction)
- [Defining Relationships](#defining-relationships)
    - [One To One](#one-to-one)
    - [One To Many](#one-to-many)
    - [One To Many (Inverse) / Belongs To](#one-to-many-inverse)
    - [Has One Of Many](#has-one-of-many)
    - [Has One Through](#has-one-through)
    - [Has Many Through](#has-many-through)
- [Many To Many Relationships](#many-to-many)
    - [Retrieving Intermediate Table Columns](#retrieving-intermediate-table-columns)
    - [Filtering Queries Via Intermediate Table Columns](#filtering-queries-via-intermediate-table-columns)
    - [Defining Custom Intermediate Table Models](#defining-custom-intermediate-table-models)
- [Polymorphic Relationships](#polymorphic-relationships)
    - [One To One](#one-to-one-polymorphic-relations)
    - [One To Many](#one-to-many-polymorphic-relations)
    - [One Of Many](#one-of-many-polymorphic-relations)
    - [Many To Many](#many-to-many-polymorphic-relations)
    - [Custom Polymorphic Types](#custom-polymorphic-types)
- [Dynamic Relationships](#dynamic-relationships)
- [Querying Relations](#querying-relations)
    - [Relationship Methods Vs. Dynamic Properties](#relationship-methods-vs-dynamic-properties)
    - [Querying Relationship Existence](#querying-relationship-existence)
    - [Querying Relationship Absence](#querying-relationship-absence)
    - [Querying Morph To Relationships](#querying-morph-to-relationships)
- [Aggregating Related Models](#aggregating-related-models)
    - [Counting Related Models](#counting-related-models)
    - [Other Aggregate Functions](#other-aggregate-functions)
    - [Counting Related Models On Morph To Relationships](#counting-related-models-on-morph-to-relationships)
- [Eager Loading](#eager-loading)
    - [Constraining Eager Loads](#constraining-eager-loads)
    - [Lazy Eager Loading](#lazy-eager-loading)
    - [Preventing Lazy Loading](#preventing-lazy-loading)
- [Inserting & Updating Related Models](#inserting-and-updating-related-models)
    - [The `save` Method](#the-save-method)
    - [The `create` Method](#the-create-method)
    - [Belongs To Relationships](#updating-belongs-to-relationships)
    - [Many To Many Relationships](#updating-many-to-many-relationships)
- [Touching Parent Timestamps](#touching-parent-timestamps)

<a name="introduction"></a>
<!-- ## Introduction -->
## Introduction

<!-- Database tables are often related to one another. For example, a blog post may have many comments or an order could be related to the user who placed it. Eloquent makes managing and working with these relationships easy, and supports a variety of common relationships: -->
데이터베이스 테이블은 서로 연관되어 있는 경우가 많습니다. 예를 들어, 하나의 블로그 게시물에는 여러 개의 댓글이 달릴 수 있고, 주문 정보는 주문을 생성한 사용자와 연결될 수 있습니다. Eloquent를 사용하면 이러한 연관관계를 아주 쉽고 편리하게 다룰 수 있으며, 아래와 같은 다양한 일반적인 연관관계를 지원합니다.

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

<!-- Eloquent relationships are defined as methods on your Eloquent model classes. Since relationships also serve as powerful [query builders](/docs/8.x/queries), defining relationships as methods provides powerful method chaining and querying capabilities. For example, we may chain additional query constraints on this `posts` relationship: -->
Eloquent에서 연관관계는 Eloquent 모델 클래스의 메서드로 정의합니다. 연관관계 또한 강력한 [query builders](/docs/8.x/queries)의 역할을 하므로, 메서드로 정의하면 메서드 체이닝과 편리한 쿼리 작성이 가능합니다. 예를 들어, 아래와 같이 `posts` 연관관계에 추가로 쿼리 조건을 연결할 수 있습니다.

```
$user->posts()->where('active', 1)->get();
```

<!-- But, before diving too deep into using relationships, let's learn how to define each type of relationship supported by Eloquent. -->
하지만 본격적으로 연관관계를 활용하기 전에, Eloquent에서 지원하는 각 연관관계 유형을 어떻게 정의하는지부터 살펴보겠습니다.

<a name="one-to-one"></a>
<!-- ### One To One -->
### One To One

<!-- A one-to-one relationship is a very basic type of database relationship. For example, a `User` model might be associated with one `Phone` model. To define this relationship, we will place a `phone` method on the `User` model. The `phone` method should call the `hasOne` method and return its result. The `hasOne` method is available to your model via the model's `Illuminate\Database\Eloquent\Model` base class: -->
일대일 연관관계는 가장 기본적인 데이터베이스 연관관계입니다. 예를 들어, `User` 모델이 `Phone` 모델 하나와 연결되어 있을 수 있습니다. 이 연관관계를 정의하려면, `User` 모델에 `phone` 메서드를 추가해서, 이 `phone` 메서드에서 `hasOne` 메서드를 호출한 결과값을 반환하면 됩니다. `hasOne` 메서드는 모델의 기본 클래스인 `Illuminate\Database\Eloquent\Model`을 통해 제공됩니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * Get the phone associated with the user.
     */
    public function phone()
    {
        return $this->hasOne(Phone::class);
    }
}
```

<!-- The first argument passed to the `hasOne` method is the name of the related model class. Once the relationship is defined, we may retrieve the related record using Eloquent's dynamic properties. Dynamic properties allow you to access relationship methods as if they were properties defined on the model: -->
`hasOne` 메서드의 첫 번째 인자는 연관된 모델의 클래스명을 전달합니다. 연관관계를 정의하면, Eloquent의 동적 속성을 사용하여 관련된 레코드를 조회할 수 있습니다. 동적 속성을 사용하면 마치 모델에 정의된 일반 속성처럼 연관관계 메서드에 접근할 수 있습니다.

```
$phone = User::find(1)->phone;
```

<!-- Eloquent determines the foreign key of the relationship based on the parent model name. In this case, the `Phone` model is automatically assumed to have a `user_id` foreign key. If you wish to override this convention, you may pass a second argument to the `hasOne` method: -->
Eloquent는 부모 모델명을 기준으로 연관된 테이블의 외래 키(foreign key)명을 자동으로 결정합니다. 위 예시에서는 `Phone` 모델이 기본적으로 `user_id` 외래키를 가진 것으로 간주합니다. 만약 이 규칙을 변경하고 싶다면, `hasOne` 메서드의 두 번째 인자로 원하는 외래 키명을 전달하면 됩니다.

```
return $this->hasOne(Phone::class, 'foreign_key');
```

<!-- Additionally, Eloquent assumes that the foreign key should have a value matching the primary key column of the parent. In other words, Eloquent will look for the value of the user's `id` column in the `user_id` column of the `Phone` record. If you would like the relationship to use a primary key value other than `id` or your model's `$primaryKey` property, you may pass a third argument to the `hasOne` method: -->
또한 Eloquent는 외래 키에 저장된 값이 부모 모델의 기본키(primary key) 컬럼 값과 일치한다고 가정합니다. 즉, Eloquent는 `Phone` 레코드의 `user_id` 컬럼에서 사용자의 `id` 컬럼 값을 찾아줍니다. 만약 `id`가 아닌 다른 컬럼을 기본키로 사용하고 싶거나, 모델의 `$primaryKey` 속성 외의 값을 사용하고 싶다면, `hasOne` 메서드의 세 번째 인자로 로컬 키(local key)를 명시하면 됩니다.

```
return $this->hasOne(Phone::class, 'foreign_key', 'local_key');
```

<a name="one-to-one-defining-the-inverse-of-the-relationship"></a>
<!-- #### Defining The Inverse Of The Relationship -->
#### Defining The Inverse Of The Relationship

<!-- So, we can access the `Phone` model from our `User` model. Next, let's define a relationship on the `Phone` model that will let us access the user that owns the phone. We can define the inverse of a `hasOne` relationship using the `belongsTo` method: -->
이제 `User` 모델에서 `Phone` 모델을 참조할 수 있습니다. 이번에는 `Phone` 모델에서 해당 폰의 주인인 사용자를 참조할 수 있도록 연관관계를 정의해보겠습니다. `hasOne`의 반대 관계인 역방향 연관관계는 `belongsTo` 메서드를 사용하여 정의합니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Phone extends Model
{
    /**
     * Get the user that owns the phone.
     */
    public function user()
    {
        return $this->belongsTo(User::class);
    }
}
```

<!-- When invoking the `user` method, Eloquent will attempt to find a `User` model that has an `id` which matches the `user_id` column on the `Phone` model. -->
`user` 메서드를 호출하면, Eloquent는 `Phone` 모델의 `user_id` 컬럼 값과 일치하는 `id`를 가진 `User` 모델을 찾아 연결해줍니다.

<!-- Eloquent determines the foreign key name by examining the name of the relationship method and suffixing the method name with `_id`. So, in this case, Eloquent assumes that the `Phone` model has a `user_id` column. However, if the foreign key on the `Phone` model is not `user_id`, you may pass a custom key name as the second argument to the `belongsTo` method: -->
Eloquent는 연관관계 메서드명을 분석하여 외래 키명을 정합니다. 일반적으로 메서드명에 `_id`를 붙여서 외래키 컬럼을 예상합니다. 즉, 위 예시에서는 Eloquent가 `Phone` 모델에 `user_id` 컬럼이 있다고 간주합니다. 만약 `Phone` 모델의 외래키가 `user_id`가 아니라면, `belongsTo` 메서드의 두 번째 인자로 외래 키명을 직접 지정할 수 있습니다.

```
/**
 * Get the user that owns the phone.
 */
public function user()
{
    return $this->belongsTo(User::class, 'foreign_key');
}
```

<!-- If the parent model does not use `id` as its primary key, or you wish to find the associated model using a different column, you may pass a third argument to the `belongsTo` method specifying the parent table's custom key: -->
부모 모델이 `id` 이외의 컬럼을 기본키로 사용하거나, 연관 모델을 다른 컬럼 기준으로 찾고 싶을 때는, `belongsTo` 메서드의 세 번째 인자로 부모 테이블의 기본키 컬럼명을 지정할 수 있습니다.

```
/**
 * Get the user that owns the phone.
 */
public function user()
{
    return $this->belongsTo(User::class, 'foreign_key', 'owner_key');
}
```

<a name="one-to-many"></a>
<!-- ### One To Many -->
### One To Many

<!-- A one-to-many relationship is used to define relationships where a single model is the parent to one or more child models. For example, a blog post may have an infinite number of comments. Like all other Eloquent relationships, one-to-many relationships are defined by defining a method on your Eloquent model: -->
일대다 연관관계는 하나의 모델(부모)이 여러 하위 모델(자식)과 관계맺을 때 사용합니다. 예를 들어, 하나의 게시글에는 무한정 많은 댓글이 달릴 수 있습니다. 다른 Eloquent 연관관계와 마찬가지로, 일대다 관계도 모델에 메서드를 정의하는 방식으로 만들 수 있습니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Post extends Model
{
    /**
     * Get the comments for the blog post.
     */
    public function comments()
    {
        return $this->hasMany(Comment::class);
    }
}
```

<!-- Remember, Eloquent will automatically determine the proper foreign key column for the `Comment` model. By convention, Eloquent will take the "snake case" name of the parent model and suffix it with `_id`. So, in this example, Eloquent will assume the foreign key column on the `Comment` model is `post_id`. -->
Eloquent는 `Comment` 모델의 외래키 컬럼명을 자동으로 결정합니다. 기본적으로, 부모 모델 이름을 스네이크 케이스(snake case) 변환 후 `_id`를 붙인 컬럼이 외래키로 사용됩니다. 이 예시라면 `Comment` 모델의 외래키 컬럼은 `post_id`가 됩니다.

<!-- Once the relationship method has been defined, we can access the [collection](/docs/8.x/eloquent-collections) of related comments by accessing the `comments` property. Remember, since Eloquent provides "dynamic relationship properties", we can access relationship methods as if they were defined as properties on the model: -->
연관관계 메서드를 정의한 후에는, `comments` 속성에 접근해 관련 댓글들의 [collection](/docs/8.x/eloquent-collections)을 조회할 수 있습니다. Eloquent의 "동적 연관 속성" 덕분에, 연관관계 메서드를 마치 모델에 정의된 속성처럼 접근할 수 있습니다.

```
use App\Models\Post;

$comments = Post::find(1)->comments;

foreach ($comments as $comment) {
    //
}
```

<!-- Since all relationships also serve as query builders, you may add further constraints to the relationship query by calling the `comments` method and continuing to chain conditions onto the query: -->
모든 연관관계는 쿼리 빌더 역할을 함께 하므로, `comments` 메서드를 호출한 뒤 조건을 체이닝해 추가 제약을 건 쿼리도 작성할 수 있습니다.

```
$comment = Post::find(1)->comments()
                    ->where('title', 'foo')
                    ->first();
```

<!-- Like the `hasOne` method, you may also override the foreign and local keys by passing additional arguments to the `hasMany` method: -->
`hasOne` 메서드와 마찬가지로, `hasMany`에도 외래키와 로컬키를 추가 인자로 전달하여 기본 키 규칙을 재정의할 수 있습니다.

```
return $this->hasMany(Comment::class, 'foreign_key');

return $this->hasMany(Comment::class, 'foreign_key', 'local_key');
```

<a name="one-to-many-inverse"></a>
<!-- ### One To Many (Inverse) / Belongs To -->
### One To Many (Inverse) / Belongs To

<!-- Now that we can access all of a post's comments, let's define a relationship to allow a comment to access its parent post. To define the inverse of a `hasMany` relationship, define a relationship method on the child model which calls the `belongsTo` method: -->
이제 게시글의 댓글을 모두 조회할 수 있게 되었으니, 댓글에서 상위 게시글(부모)을 참조하는 연관관계도 만들어보겠습니다. `hasMany`의 반대로, 자식 모델에서 부모 모델을 바라보게 하려면 `belongsTo` 메서드를 이용해 연관관계 메서드를 정의하면 됩니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Comment extends Model
{
    /**
     * Get the post that owns the comment.
     */
    public function post()
    {
        return $this->belongsTo(Post::class);
    }
}
```

<!-- Once the relationship has been defined, we can retrieve a comment's parent post by accessing the `post` "dynamic relationship property": -->
이제 연관관계가 정의되었으니, 댓글 인스턴스에서 부모 게시글을 `post` "동적 연관관계 속성"으로 접근할 수 있습니다.

```
use App\Models\Comment;

$comment = Comment::find(1);

return $comment->post->title;
```

<!-- In the example above, Eloquent will attempt to find a `Post` model that has an `id` which matches the `post_id` column on the `Comment` model. -->
위 예시에서 Eloquent는 `Comment` 모델의 `post_id` 컬럼 값과 일치하는 `id`를 가진 `Post` 모델을 찾아 연결합니다.

<!-- Eloquent determines the default foreign key name by examining the name of the relationship method and suffixing the method name with a `_` followed by the name of the parent model's primary key column. So, in this example, Eloquent will assume the `Post` model's foreign key on the `comments` table is `post_id`. -->
Eloquent는 연관관계 메서드명을 기준으로, `_`와 부모 모델의 기본키 컬럼명을 조합해 외래키 컬럼명을 정합니다. 이 예시에서는 `comments` 테이블에 대한 `Post` 모델의 외래키가 `post_id`로 간주됩니다.

<!-- However, if the foreign key for your relationship does not follow these conventions, you may pass a custom foreign key name as the second argument to the `belongsTo` method: -->
하지만, 연관관계의 외래키 이름이 이 규칙을 따르지 않는 경우라면 `belongsTo` 메서드의 두 번째 인자로 직접 외래키 이름을 지정할 수 있습니다.

```
/**
 * Get the post that owns the comment.
 */
public function post()
{
    return $this->belongsTo(Post::class, 'foreign_key');
}
```

<!-- If your parent model does not use `id` as its primary key, or you wish to find the associated model using a different column, you may pass a third argument to the `belongsTo` method specifying your parent table's custom key: -->
마찬가지로 부모 모델이 `id`가 아닌 다른 컬럼을 기본키로 사용하거나, 연관 모델을 다른 기준 컬럼으로 찾고 싶다면 `belongsTo` 메서드의 세 번째 인자로 지정할 수 있습니다.

```
/**
 * Get the post that owns the comment.
 */
public function post()
{
    return $this->belongsTo(Post::class, 'foreign_key', 'owner_key');
}
```

<a name="default-models"></a>
<!-- #### Default Models -->
#### Default Models

<!-- The `belongsTo`, `hasOne`, `hasOneThrough`, and `morphOne` relationships allow you to define a default model that will be returned if the given relationship is `null`. This pattern is often referred to as the [Null Object pattern](https://en.wikipedia.org/wiki/Null_Object_pattern) and can help remove conditional checks in your code. In the following example, the `user` relation will return an empty `App\Models\User` model if no user is attached to the `Post` model: -->
`belongsTo`, `hasOne`, `hasOneThrough`, `morphOne` 연관관계에서는 해당 관계가 `null`일 때 반환할 기본 모델을 정의할 수 있습니다. 이 패턴은 흔히 [Null Object pattern](https://en.wikipedia.org/wiki/Null_Object_pattern)이라 불리며, 코드에서 조건문 검사를 줄이는 데 도움이 됩니다. 아래 예시에서는 `Post` 모델이 `user` 모델과 연결되어 있지 않더라도, 빈 `App\Models\User` 모델이 반환됩니다.

```
/**
 * Get the author of the post.
 */
public function user()
{
    return $this->belongsTo(User::class)->withDefault();
}
```

<!-- To populate the default model with attributes, you may pass an array or closure to the `withDefault` method: -->
기본 모델을 특정 속성값으로 채우고 싶을 때는, `withDefault` 메서드에 배열이나 클로저를 전달할 수 있습니다.

```
/**
 * Get the author of the post.
 */
public function user()
{
    return $this->belongsTo(User::class)->withDefault([
        'name' => 'Guest Author',
    ]);
}

/**
 * Get the author of the post.
 */
public function user()
{
    return $this->belongsTo(User::class)->withDefault(function ($user, $post) {
        $user->name = 'Guest Author';
    });
}
```

<a name="querying-belongs-to-relationships"></a>
<!-- #### Querying Belongs To Relationships -->
#### Querying Belongs To Relationships

<!-- When querying for the children of a "belongs to" relationship, you may manually build the `where` clause to retrieve the corresponding Eloquent models: -->
"Belongs To" 관계의 하위 모델을 쿼리할 때, `where` 절을 직접 작성해서 해당하는 Eloquent 모델을 조회할 수 있습니다.

```
use App\Models\Post;

$posts = Post::where('user_id', $user->id)->get();
```

<!-- However, you may find it more convenient to use the `whereBelongsTo` method, which will automatically determine the proper relationship and foreign key for the given model: -->
하지만 이보다 더 편리하게, `whereBelongsTo` 메서드를 사용하면 모델과 연관된 관계 및 외래키를 자동으로 판단하여 쿼리를 만들어줍니다.

```
$posts = Post::whereBelongsTo($user)->get();
```

<!-- By default, Laravel will determine the relationship associated with the given model based on the class name of the model; however, you may specify the relationship name manually by providing it as the second argument to the `whereBelongsTo` method: -->
기본적으로 Laravel은 전달된 모델의 클래스명을 기준으로 연관관계를 찾아줍니다. 하지만, `whereBelongsTo` 메서드의 두 번째 인자로 연관관계명을 직접 지정할 수도 있습니다.

```
$posts = Post::whereBelongsTo($user, 'author')->get();
```

<a name="has-one-of-many"></a>
<!-- ### Has One Of Many -->
### Has One Of Many

<!-- Sometimes a model may have many related models, yet you want to easily retrieve the "latest" or "oldest" related model of the relationship. For example, a `User` model may be related to many `Order` models, but you want to define a convenient way to interact with the most recent order the user has placed. You may accomplish this using the `hasOne` relationship type combined with the `ofMany` methods: -->
어떤 모델이 여러 연관 모델을 가질 때, 그 중에서 "가장 최근" 혹은 "가장 오래된" 한 개의 연관 모델을 편리하게 가져오고 싶을 때가 있습니다. 예를 들어, `User` 모델은 여러 개의 `Order`와 관계가 있지만, 가장 최근 주문만 간편하게 조회하고 싶을 수 있습니다. 이럴 때는 `hasOne`과 `ofMany` 메서드를 조합해서 사용하면 됩니다.

```php
/**
 * Get the user's most recent order.
 */
public function latestOrder()
{
    return $this->hasOne(Order::class)->latestOfMany();
}
```

<!-- Likewise, you may define a method to retrieve the "oldest", or first, related model of a relationship: -->
마찬가지로, "가장 오래된" 즉, 가장 먼저 생성된 연관 모델도 아래와 같이 가져올 수 있습니다.

```php
/**
 * Get the user's oldest order.
 */
public function oldestOrder()
{
    return $this->hasOne(Order::class)->oldestOfMany();
}
```

<!-- By default, the `latestOfMany` and `oldestOfMany` methods will retrieve the latest or oldest related model based on the model's primary key, which must be sortable. However, sometimes you may wish to retrieve a single model from a larger relationship using a different sorting criteria. -->
기본적으로 `latestOfMany`와 `oldestOfMany`는 모델의 기본키(primary key)를 오름차순 또는 내림차순으로 정렬해 가장 최근 혹은 가장 오래된 레코드를 반환합니다. (기본키는 정렬이 가능한 값이어야 합니다.) 하지만 때로는 다른 컬럼을 기준으로 특정 모델을 선택해야 할 수도 있습니다.

<!-- For example, using the `ofMany` method, you may retrieve the user's most expensive order. The `ofMany` method accepts the sortable column as its first argument and which aggregate function (`min` or `max`) to apply when querying for the related model: -->
예를 들어, `ofMany` 메서드를 활용해 사용자의 가장 비싼 주문을 조회할 수도 있습니다. `ofMany`의 첫 번째 인자로 정렬에 사용할 컬럼명을, 두 번째 인자로 적용할 집계 함수(`min` 또는 `max`)를 지정합니다.

```php
/**
 * Get the user's largest order.
 */
public function largestOrder()
{
    return $this->hasOne(Order::class)->ofMany('price', 'max');
}
```

> [!NOTE]
> PostgreSQL은 UUID 컬럼에 대해 `MAX` 함수를 지원하지 않으므로, PostgreSQL UUID 컬럼과 one-of-many 관계를 조합해서는 사용할 수 없습니다.

<a name="advanced-has-one-of-many-relationships"></a>
<!-- #### Advanced Has One Of Many Relationships -->
#### Advanced Has One Of Many Relationships

<!-- It is possible to construct more advanced "has one of many" relationships. For example, A `Product` model may have many associated `Price` models that are retained in the system even after new pricing is published. In addition, new pricing data for the product may be able to be published in advance to take effect at a future date via a `published_at` column. -->
더 복잡한 "has one of many" 연관관계도 만들 수 있습니다. 예를 들어, `Product` 모델이 여러 개의 `Price` 모델과 관계를 맺고 있고, 새로운 가격 정보가 미리 등록되어 미래의 특정 시점부터 적용될 수 있다고 해보겠습니다. 이때는 `published_at` 컬럼을 활용해 미래가 아닌, 이미 퍼블리싱된 최신 가격만 조회해야 합니다. 또한, 같은 퍼블리시 날짜라면 id값이 가장 큰 가격을 우선시한다고 가정합시다.

<!-- So, in summary, we need to retrieve the latest published pricing where the published date is not in the future. In addition, if two prices have the same published date, we will prefer the price with the greatest ID. To accomplish this, we must pass an array to the `ofMany` method that contains the sortable columns which determine the latest price. In addition, a closure will be provided as the second argument to the `ofMany` method. This closure will be responsible for adding additional publish date constraints to the relationship query: -->
이렇게 여러 기준을 활용하려면, `ofMany` 메서드에 가장 최신 가격을 결정하는 정렬 컬럼들을 배열로 전달하고, `ofMany` 메서드의 두 번째 인자에 추가 발행일 조건을 담은 클로저를 정의하면 됩니다.

```php
/**
 * Get the current pricing for the product.
 */
public function currentPricing()
{
    return $this->hasOne(Price::class)->ofMany([
        'published_at' => 'max',
        'id' => 'max',
    ], function ($query) {
        $query->where('published_at', '<', now());
    });
}
```

<a name="has-one-through"></a>
<!-- ### Has One Through -->
### Has One Through

<!-- The "has-one-through" relationship defines a one-to-one relationship with another model. However, this relationship indicates that the declaring model can be matched with one instance of another model by proceeding _through_ a third model. -->
"has-one-through" 관계는 최종적으로 한 개의 다른 모델과 일대일 관계를 맺지만, 그 사이에 중간 모델을 한 번 거쳐야 할 때 사용합니다.

<!-- For example, in a vehicle repair shop application, each `Mechanic` model may be associated with one `Car` model, and each `Car` model may be associated with one `Owner` model. While the mechanic and the owner have no direct relationship within the database, the mechanic can access the owner _through_ the `Car` model. Let's look at the tables necessary to define this relationship: -->
예를 들어, 자동차 수리소 애플리케이션에서 `Mechanic` 모델과 `Car` 모델이 1:1 관계이고, `Car`와 `Owner` 모델도 1:1 관계라고 해봅시다. 이 경우 정비공과 차의 소유주는 DB상 직접적인 관계가 없지만, 정비공은 `Car` 모델을 통해 소유주 모델에 접근할 수 있습니다. 관련 테이블 구조는 아래와 같습니다.

```
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
테이블 구조를 살펴봤으니, 이제 `Mechanic` 모델에 관계를 정의해봅시다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Mechanic extends Model
{
    /**
     * Get the car's owner.
     */
    public function carOwner()
    {
        return $this->hasOneThrough(Owner::class, Car::class);
    }
}
```

<!-- The first argument passed to the `hasOneThrough` method is the name of the final model we wish to access, while the second argument is the name of the intermediate model. -->
`hasOneThrough`의 첫 번째 인자는 최종적으로 접근할 모델, 두 번째 인자는 중간에 거치는 모델의 클래스명을 전달합니다.

<a name="has-one-through-key-conventions"></a>
<!-- #### Key Conventions -->
#### Key Conventions

<!-- Typical Eloquent foreign key conventions will be used when performing the relationship's queries. If you would like to customize the keys of the relationship, you may pass them as the third and fourth arguments to the `hasOneThrough` method. The third argument is the name of the foreign key on the intermediate model. The fourth argument is the name of the foreign key on the final model. The fifth argument is the local key, while the sixth argument is the local key of the intermediate model: -->
기본적으로 Eloquent는 외래키 명명 규칙을 활용해 쿼리를 작성합니다. 만약 관계에 사용할 키를 직접 커스터마이징하고 싶다면, `hasOneThrough` 메서드의 세 번째와 네 번째 인자로 키명을 넘기면 됩니다. 세 번째 인자는 중간 모델(예: cars)의 외래키, 네 번째 인자는 최종 모델(owners)의 외래키, 다섯 번째 인자는 mechanics 테이블의 로컬키, 여섯 번째 인자는 cars 테이블의 로컬키입니다.

```
class Mechanic extends Model
{
    /**
     * Get the car's owner.
     */
    public function carOwner()
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

<a name="has-many-through"></a>
<!-- ### Has Many Through -->
### Has Many Through

<!-- The "has-many-through" relationship provides a convenient way to access distant relations via an intermediate relation. For example, let's assume we are building a deployment platform like [Laravel Vapor](https://vapor.laravel.com). A `Project` model might access many `Deployment` models through an intermediate `Environment` model. Using this example, you could easily gather all deployments for a given project. Let's look at the tables required to define this relationship: -->
"has-many-through" 관계는 중간 모델을 통해 먼 거리의 연관 데이터를 간편하게 액세스할 수 있게 해줍니다. 예를 들어, [Laravel Vapor](https://vapor.laravel.com)와 같은 배포 플랫폼을 만든다고 가정합니다. `Project` 모델에서 중간에 있는 `Environment` 모델을 거쳐, 여러 개의 `Deployment` 모델을 연결해야 할 수 있습니다. 아래와 같은 테이블 구조가 필요합니다.

```
projects
    id - integer
    name - string

environments
    id - integer
    project_id - integer
    name - string

deployments
    id - integer
    environment_id - integer
    commit_hash - string
```

<!-- Now that we have examined the table structure for the relationship, let's define the relationship on the `Project` model: -->
이제 테이블 구조를 살펴봤으니, `Project` 모델에서 연관관계를 아래와 같이 정의할 수 있습니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Project extends Model
{
    /**
     * Get all of the deployments for the project.
     */
    public function deployments()
    {
        return $this->hasManyThrough(Deployment::class, Environment::class);
    }
}
```

<!-- The first argument passed to the `hasManyThrough` method is the name of the final model we wish to access, while the second argument is the name of the intermediate model. -->
`hasManyThrough` 메서드의 첫 번째 인자로 최종적으로 접근할 모델명을, 두 번째 인자로 중간 모델명을 전달합니다.

<!-- Though the `Deployment` model's table does not contain a `project_id` column, the `hasManyThrough` relation provides access to a project's deployments via `$project->deployments`. To retrieve these models, Eloquent inspects the `project_id` column on the intermediate `Environment` model's table. After finding the relevant environment IDs, they are used to query the `Deployment` model's table. -->
`Deployment` 모델의 테이블에는 `project_id` 컬럼이 존재하지 않지만, `hasManyThrough` 관계를 활용하면 `$project->deployments`로 해당 프로젝트의 모든 배포를 손쉽게 조회할 수 있습니다. 이를 위해 Eloquent는 `Environment` 모델의 `project_id` 컬럼을 활용해 관련 환경들의 id를 찾고, 이 id들을 기준으로 `Deployment` 데이터를 조회합니다.

<a name="has-many-through-key-conventions"></a>
<!-- #### Key Conventions -->
#### Key Conventions

<!-- Typical Eloquent foreign key conventions will be used when performing the relationship's queries. If you would like to customize the keys of the relationship, you may pass them as the third and fourth arguments to the `hasManyThrough` method. The third argument is the name of the foreign key on the intermediate model. The fourth argument is the name of the foreign key on the final model. The fifth argument is the local key, while the sixth argument is the local key of the intermediate model: -->
Eloquent의 기본 외래키 네이밍 규칙이 여기서도 사용됩니다. 만약 직접 키를 지정하고 싶다면, `hasManyThrough` 메서드의 세 번째, 네 번째 인자를 사용하세요. 세 번째 인자는 중간 모델(environments)의 외래키, 네 번째 인자는 최종 모델(deployments)의 외래키, 다섯 번째 인자는 projects 테이블의 로컬키, 여섯 번째 인자는 environments 테이블의 로컬키입니다.

```
class Project extends Model
{
    public function deployments()
    {
        return $this->hasManyThrough(
            Deployment::class,
            Environment::class,
            'project_id', // Foreign key on the environments table...
            'environment_id', // Foreign key on the deployments table...
            'id', // Local key on the projects table...
            'id' // Local key on the environments table...
        );
    }
}
```

<a name="many-to-many"></a>
<!-- ## Many To Many Relationships -->
## Many To Many Relationships

<!-- Many-to-many relations are slightly more complicated than `hasOne` and `hasMany` relationships. An example of a many-to-many relationship is a user that has many roles and those roles are also shared by other users in the application. For example, a user may be assigned the role of "Author" and "Editor"; however, those roles may also be assigned to other users as well. So, a user has many roles and a role has many users. -->
다대다(many-to-many) 관계는 `hasOne`이나 `hasMany`에 비해 다소 복잡할 수 있습니다. 대표적인 예로 사용자가 여러 역할(role)을 가질 수 있고, 그 역할이 여러 사용자에게 공유되는 경우를 들 수 있습니다. 예를 들어 어떤 사용자는 "Author"와 "Editor" 역할을 가질 수 있지만, 이 역할은 다른 사용자에도 할당될 수 있습니다. 즉, 한 사용자가 여러 역할을 가질 수 있고, 한 역할도 여러 사용자와 연관될 수 있습니다.

<a name="many-to-many-table-structure"></a>
<!-- #### Table Structure -->
#### Table Structure

<!-- To define this relationship, three database tables are needed: `users`, `roles`, and `role_user`. The `role_user` table is derived from the alphabetical order of the related model names and contains `user_id` and `role_id` columns. This table is used as an intermediate table linking the users and roles. -->
이 관계를 정의하려면 세 개의 데이터베이스 테이블이 필요합니다: `users`, `roles`, 그리고 `role_user`입니다. `role_user` 테이블은 연관 모델 이름을 알파벳순으로 조합한 이름이며, `user_id`와 `role_id` 컬럼을 포함합니다. 이 테이블은 사용자와 역할을 연결해주는 중간 역할을 합니다.

<!-- Remember, since a role can belong to many users, we cannot simply place a `user_id` column on the `roles` table. This would mean that a role could only belong to a single user. In order to provide support for roles being assigned to multiple users, the `role_user` table is needed. We can summarize the relationship's table structure like so: -->
한 역할이 여러 사용자와 연결될 수 있으므로, `roles` 테이블에 단순히 `user_id` 컬럼을 추가할 수는 없습니다. 그럴 경우 하나의 역할이 한 명의 사용자와만 연결될 수 있기 때문입니다. 여러 사용자가 역할을 공유할 수 있도록 하기 위해 별도의 중간 테이블(`role_user`)이 필요합니다. 테이블 구조를 정리하면 아래와 같습니다.

```
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
다대다(many-to-many) 연관관계는 `belongsToMany` 메서드의 반환값을 리턴하는 메서드를 작성하여 정의합니다. `belongsToMany` 메서드는 애플리케이션의 모든 Eloquent 모델이 상속받는 `Illuminate\Database\Eloquent\Model` 기본 클래스에서 제공됩니다. 예를 들어, `User` 모델에 `roles` 메서드를 정의해보겠습니다. 이 메서드의 첫 번째 인수에는 연관된 모델 클래스명을 전달합니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * The roles that belong to the user.
     */
    public function roles()
    {
        return $this->belongsToMany(Role::class);
    }
}
```

<!-- Once the relationship is defined, you may access the user's roles using the `roles` dynamic relationship property: -->
이렇게 연관관계를 정의한 후에는, `roles`라는 동적 연관관계 프로퍼티를 통해 사용자의 역할 목록을 조회할 수 있습니다.

```
use App\Models\User;

$user = User::find(1);

foreach ($user->roles as $role) {
    //
}
```

<!-- Since all relationships also serve as query builders, you may add further constraints to the relationship query by calling the `roles` method and continuing to chain conditions onto the query: -->
모든 연관관계 메서드는 쿼리 빌더 역할도 하기 때문에, `roles` 메서드를 호출하고 이어서 조건을 체이닝하여 연관관계에 추가적인 제한을 걸 수 있습니다.

```
$roles = User::find(1)->roles()->orderBy('name')->get();
```

<!-- To determine the table name of the relationship's intermediate table, Eloquent will join the two related model names in alphabetical order. However, you are free to override this convention. You may do so by passing a second argument to the `belongsToMany` method: -->
연관관계를 위한 중간 테이블의 이름을 결정할 때, Eloquent는 두 모델의 이름을 알파벳순으로 결합해 생성합니다. 그러나 이 방식은 자유롭게 재정의할 수 있습니다. 중간 테이블명을 직접 지정하려면, `belongsToMany` 메서드의 두 번째 인수로 테이블명을 전달하면 됩니다.

```
return $this->belongsToMany(Role::class, 'role_user');
```

<!-- In addition to customizing the name of the intermediate table, you may also customize the column names of the keys on the table by passing additional arguments to the `belongsToMany` method. The third argument is the foreign key name of the model on which you are defining the relationship, while the fourth argument is the foreign key name of the model that you are joining to: -->
중간 테이블의 이름뿐만 아니라, `belongsToMany` 메서드에 추가 인수를 전달하여 테이블 내에서 사용할 외래 키의 컬럼명도 커스터마이즈할 수 있습니다. 세 번째 인수는 현재 연관관계를 정의하고 있는 모델의 외래 키 컬럼명이고, 네 번째 인수는 조인하려는 모델의 외래 키 컬럼명입니다.

```
return $this->belongsToMany(Role::class, 'role_user', 'user_id', 'role_id');
```

<a name="many-to-many-defining-the-inverse-of-the-relationship"></a>
<!-- #### Defining The Inverse Of The Relationship -->
#### Defining The Inverse Of The Relationship

<!-- To define the "inverse" of a many-to-many relationship, you should define a method on the related model which also returns the result of the `belongsToMany` method. To complete our user / role example, let's define the `users` method on the `Role` model: -->
다대다 연관관계의 "반대편"을 정의하려면, 연관된 모델에 역시 `belongsToMany` 메서드의 반환값을 리턴하는 메서드를 정의하면 됩니다. 사용자/역할 예제를 완성해보면, 이번에는 `Role` 모델에 `users` 메서드를 정의할 수 있습니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Role extends Model
{
    /**
     * The users that belong to the role.
     */
    public function users()
    {
        return $this->belongsToMany(User::class);
    }
}
```

<!-- As you can see, the relationship is defined exactly the same as its `User` model counterpart with the exception of referencing the `App\Models\User` model. Since we're reusing the `belongsToMany` method, all of the usual table and key customization options are available when defining the "inverse" of many-to-many relationships. -->
보시다시피, 연관관계는 기본적으로 `User` 모델에서 정의한 방식과 거의 동일하지만, 참조하는 모델만 `App\Models\User`로 다릅니다. 동일하게 `belongsToMany` 메서드를 활용하기 때문에, 다대다 연관관계의 "반대편"을 정의할 때도 테이블과 키를 커스터마이즈할 수 있는 모든 옵션을 사용할 수 있습니다.

<a name="retrieving-intermediate-table-columns"></a>
<!-- ### Retrieving Intermediate Table Columns -->
### Retrieving Intermediate Table Columns

<!-- As you have already learned, working with many-to-many relations requires the presence of an intermediate table. Eloquent provides some very helpful ways of interacting with this table. For example, let's assume our `User` model has many `Role` models that it is related to. After accessing this relationship, we may access the intermediate table using the `pivot` attribute on the models: -->
이미 배운 것처럼, 다대다 연결을 다루려면 중간 테이블이 필요합니다. Eloquent는 이 중간 테이블과 쉽게 상호작용할 수 있는 다양한 방법을 제공합니다. 예를 들어, `User` 모델이 여러 `Role` 모델과 연관되어 있다고 가정해 보겠습니다. 연관관계를 조회한 후에는, 모델의 `pivot` 속성을 이용해 중간 테이블의 데이터를 접근할 수 있습니다.

```
use App\Models\User;

$user = User::find(1);

foreach ($user->roles as $role) {
    echo $role->pivot->created_at;
}
```

<!-- Notice that each `Role` model we retrieve is automatically assigned a `pivot` attribute. This attribute contains a model representing the intermediate table. -->
각 `Role` 모델에는 자동으로 `pivot` 속성이 할당됩니다. 이 속성에는 중간 테이블을 대표하는 모델 인스턴스가 담깁니다.

<!-- By default, only the model keys will be present on the `pivot` model. If your intermediate table contains extra attributes, you must specify them when defining the relationship: -->
기본적으로 `pivot` 모델에는 두 관련 모델의 키만 포함됩니다. 만약 중간 테이블에 추가적인 속성이 있다면, 연관관계를 정의할 때 해당 속성들을 명시해야 합니다.

```
return $this->belongsToMany(Role::class)->withPivot('active', 'created_by');
```

<!-- If you would like your intermediate table to have `created_at` and `updated_at` timestamps that are automatically maintained by Eloquent, call the `withTimestamps` method when defining the relationship: -->
Eloquent가 중간 테이블의 `created_at` 및 `updated_at` 타임스탬프를 자동으로 관리하게 하고 싶다면, 연관관계를 정의할 때 `withTimestamps` 메서드를 호출하면 됩니다.

```
return $this->belongsToMany(Role::class)->withTimestamps();
```

> [!NOTE]
> Eloquent의 자동화된 타임스탬프를 사용하는 중간 테이블에는 반드시 `created_at`과 `updated_at` 컬럼이 모두 존재해야 합니다.

<a name="customizing-the-pivot-attribute-name"></a>
<!-- #### Customizing The `pivot` Attribute Name -->
#### Customizing The `pivot` Attribute Name

<!-- As noted previously, attributes from the intermediate table may be accessed on models via the `pivot` attribute. However, you are free to customize the name of this attribute to better reflect its purpose within your application. -->
앞서 설명했듯이, 중간 테이블의 컬럼 값은 모델의 `pivot` 속성을 통해 접근할 수 있습니다. 하지만 애플리케이션의 용도에 맞게 이 속성명을 좀 더 의미 있게 변경할 수 있습니다.

<!-- For example, if your application contains users that may subscribe to podcasts, you likely have a many-to-many relationship between users and podcasts. If this is the case, you may wish to rename your intermediate table attribute to `subscription` instead of `pivot`. This can be done using the `as` method when defining the relationship: -->
예를 들어, 사용자가 팟캐스트를 구독할 수 있는 시스템이라면 사용자와 팟캐스트는 다대다 관계를 갖습니다. 이런 경우, `pivot` 대신 `subscription` 같은 이름으로 중간 테이블 속성명을 변경하고 싶을 수 있습니다. 이럴 때는 연관관계 정의 시 `as` 메서드를 사용하면 됩니다.

```
return $this->belongsToMany(Podcast::class)
                ->as('subscription')
                ->withTimestamps();
```

<!-- Once the custom intermediate table attribute has been specified, you may access the intermediate table data using the customized name: -->
이렇게 중간 테이블 속성명을 커스터마이즈한 이후에는, 해당 이름으로 중간 테이블 데이터를 접근할 수 있습니다.

```
$users = User::with('podcasts')->get();

foreach ($users->flatMap->podcasts as $podcast) {
    echo $podcast->subscription->created_at;
}
```

<a name="filtering-queries-via-intermediate-table-columns"></a>
<!-- ### Filtering Queries Via Intermediate Table Columns -->
### Filtering Queries Via Intermediate Table Columns

<!-- You can also filter the results returned by `belongsToMany` relationship queries using the `wherePivot`, `wherePivotIn`, `wherePivotNotIn`, `wherePivotBetween`, `wherePivotNotBetween`, `wherePivotNull`, and `wherePivotNotNull` methods when defining the relationship: -->
`wherePivot`, `wherePivotIn`, `wherePivotNotIn`, `wherePivotBetween`, `wherePivotNotBetween`, `wherePivotNull`, `wherePivotNotNull` 등의 메서드를 사용하면, `belongsToMany` 연관관계 쿼리 결과를 중간 테이블의 컬럼값을 기준으로 필터링할 수 있습니다.

```
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

<a name="defining-custom-intermediate-table-models"></a>
<!-- ### Defining Custom Intermediate Table Models -->
### Defining Custom Intermediate Table Models

<!-- If you would like to define a custom model to represent the intermediate table of your many-to-many relationship, you may call the `using` method when defining the relationship. Custom pivot models give you the opportunity to define additional methods on the pivot model. -->
다대다 연관관계의 중간 테이블을 표현하는 커스텀 모델을 정의하고 싶다면, 연관관계 정의 시 `using` 메서드를 사용하면 됩니다. 커스텀 피벗(pivot) 모델을 활용하면, 피벗 모델에 추가적인 메서드도 정의할 수 있습니다.

<!-- Custom many-to-many pivot models should extend the `Illuminate\Database\Eloquent\Relations\Pivot` class while custom polymorphic many-to-many pivot models should extend the `Illuminate\Database\Eloquent\Relations\MorphPivot` class. For example, we may define a `Role` model which uses a custom `RoleUser` pivot model: -->
커스텀 다대다 피벗 모델은 반드시 `Illuminate\Database\Eloquent\Relations\Pivot` 클래스를 상속해야 하고, 커스텀 다형 다대다 피벗 모델은 `Illuminate\Database\Eloquent\Relations\MorphPivot` 클래스를 상속해야 합니다. 예를 들어, `Role` 모델에서 커스텀 `RoleUser` 피벗 모델을 사용하는 코드는 다음과 같습니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Role extends Model
{
    /**
     * The users that belong to the role.
     */
    public function users()
    {
        return $this->belongsToMany(User::class)->using(RoleUser::class);
    }
}
```

<!-- When defining the `RoleUser` model, you should extend the `Illuminate\Database\Eloquent\Relations\Pivot` class: -->
`RoleUser` 모델을 정의할 때는 `Illuminate\Database\Eloquent\Relations\Pivot` 클래스를 상속해야 합니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Relations\Pivot;

class RoleUser extends Pivot
{
    //
}
```

> [!NOTE]
> 피벗 모델에는 `SoftDeletes` 트레이트를 사용할 수 없습니다. 피벗 레코드에 소프트 삭제 기능이 필요하다면 피벗 모델 대신 실제 Eloquent 모델로 전환하는 방식을 고려하세요.

<a name="custom-pivot-models-and-incrementing-ids"></a>
<!-- #### Custom Pivot Models And Incrementing IDs -->
#### Custom Pivot Models And Incrementing IDs

<!-- If you have defined a many-to-many relationship that uses a custom pivot model, and that pivot model has an auto-incrementing primary key, you should ensure your custom pivot model class defines an `incrementing` property that is set to `true`. -->
만약 커스텀 피벗 모델에서 자동 증가(primary key auto-increment)되는 ID 컬럼을 사용한다면, 해당 모델 클래스 내에 `incrementing` 속성을 반드시 `true`로 지정해야 합니다.

```
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
다형적(polymorphic) 관계란 하나의 자식 모델이 단일 연관관계를 통해 여러 종류의 다른 모델에 속할 수 있도록 하는 방식입니다. 예를 들어, 사용자가 블로그 글과 영상을 공유하는 애플리케이션을 만든다고 가정해 봅시다. 이때 `Comment` 모델은 `Post`와 `Video` 모델 모두와 관계를 맺을 수 있습니다.

<a name="one-to-one-polymorphic-relations"></a>
<!-- ### One To One (Polymorphic) -->
### One To One (Polymorphic)

<a name="one-to-one-polymorphic-table-structure"></a>
<!-- #### Table Structure -->
#### Table Structure

<!-- A one-to-one polymorphic relation is similar to a typical one-to-one relation; however, the child model can belong to more than one type of model using a single association. For example, a blog `Post` and a `User` may share a polymorphic relation to an `Image` model. Using a one-to-one polymorphic relation allows you to have a single table of unique images that may be associated with posts and users. First, let's examine the table structure: -->
일대일 다형적 관계는 일반적인 일대일 관계와 비슷하지만, 자식 모델이 단일 연관관계를 통해 다양한 종류의 부모 모델에 속할 수 있다는 점이 다릅니다. 예를 들어, 블로그 `Post`와 `User`가 하나의 `Image` 모델과 다형적 관계를 맺을 수 있습니다. 일대일 다형적 관계를 활용하면, 여러 게시글이나 사용자가 고유한 이미지들을 한 테이블에서 공유하면서 관리할 수 있습니다. 테이블 구조 예시는 다음과 같습니다.

```
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
`images` 테이블의 `imageable_id`와 `imageable_type` 컬럼을 주목하세요. `imageable_id`에는 해당 이미지의 부모가 되는 게시글 또는 사용자의 ID가 저장되고, `imageable_type`에는 부모 모델의 클래스명이 저장됩니다. `imageable` 관계에 접근할 때, Eloquent는 이 `imageable_type` 컬럼을 사용해 어떤 "종류"의 부모 모델을 반환해야 하는지 결정합니다. 이 경우, 컬럼 값은 `App\Models\Post` 또는 `App\Models\User`가 됩니다.

<a name="one-to-one-polymorphic-model-structure"></a>
<!-- #### Model Structure -->
#### Model Structure

<!-- Next, let's examine the model definitions needed to build this relationship: -->
이 연관관계를 구축하기 위해 필요한 모델 정의는 다음과 같습니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Image extends Model
{
    /**
     * Get the parent imageable model (user or post).
     */
    public function imageable()
    {
        return $this->morphTo();
    }
}

class Post extends Model
{
    /**
     * Get the post's image.
     */
    public function image()
    {
        return $this->morphOne(Image::class, 'imageable');
    }
}

class User extends Model
{
    /**
     * Get the user's image.
     */
    public function image()
    {
        return $this->morphOne(Image::class, 'imageable');
    }
}
```

<a name="one-to-one-polymorphic-retrieving-the-relationship"></a>
<!-- #### Retrieving The Relationship -->
#### Retrieving The Relationship

<!-- Once your database table and models are defined, you may access the relationships via your models. For example, to retrieve the image for a post, we can access the `image` dynamic relationship property: -->
데이터베이스 테이블과 모델이 준비되었다면, 이제 모델에서 연관관계를 직접 활용할 수 있습니다. 예를 들어, 게시글에 연관된 이미지를 조회하려면 `image`라는 동적 연관관계 프로퍼티를 사용할 수 있습니다.

```
use App\Models\Post;

$post = Post::find(1);

$image = $post->image;
```

<!-- You may retrieve the parent of the polymorphic model by accessing the name of the method that performs the call to `morphTo`. In this case, that is the `imageable` method on the `Image` model. So, we will access that method as a dynamic relationship property: -->
다형적 모델의 부모를 조회하려면, `morphTo`를 호출하는 메서드명을 동적 연관관계 프로퍼티로 접근하면 됩니다. 여기서는 `Image` 모델의 `imageable` 메서드가 해당 역할을 하므로, 아래처럼 사용합니다.

```
use App\Models\Image;

$image = Image::find(1);

$imageable = $image->imageable;
```

<!-- The `imageable` relation on the `Image` model will return either a `Post` or `User` instance, depending on which type of model owns the image. -->
`Image` 모델의 `imageable` 연관관계는 실제 이미지를 소유한 모델이 `Post`인지 `User`인지에 따라 각각의 인스턴스를 반환합니다.

<a name="morph-one-to-one-key-conventions"></a>
<!-- #### Key Conventions -->
#### Key Conventions

<!-- If necessary, you may specify the name of the "id" and "type" columns utilized by your polymorphic child model. If you do so, ensure that you always pass the name of the relationship as the first argument to the `morphTo` method. Typically, this value should match the method name, so you may use PHP's `__FUNCTION__` constant: -->
필요하다면, 다형적 자식 모델에 사용되는 "id"와 "type" 컬럼의 이름을 직접 지정할 수도 있습니다. 이때는 반드시 `morphTo` 메서드의 첫 번째 인수로 연관관계명을 전달해야 합니다. 보통 이 값은 메서드명과 일치해야 하므로, PHP의 `__FUNCTION__` 상수를 활용할 수 있습니다.

```
/**
 * Get the model that the image belongs to.
 */
public function imageable()
{
    return $this->morphTo(__FUNCTION__, 'imageable_type', 'imageable_id');
}
```

<a name="one-to-many-polymorphic-relations"></a>
<!-- ### One To Many (Polymorphic) -->
### One To Many (Polymorphic)

<a name="one-to-many-polymorphic-table-structure"></a>
<!-- #### Table Structure -->
#### Table Structure

<!-- A one-to-many polymorphic relation is similar to a typical one-to-many relation; however, the child model can belong to more than one type of model using a single association. For example, imagine users of your application can "comment" on posts and videos. Using polymorphic relationships, you may use a single `comments` table to contain comments for both posts and videos. First, let's examine the table structure required to build this relationship: -->
일대다 다형적 관계는 기본적인 일대다 관계와 비슷하지만, 자식 모델이 하나의 연관관계를 통해 여러 종류의 부모 모델에 속할 수 있습니다. 예를 들어, 애플리케이션의 사용자들이 '게시글'과 '비디오'에 모두 "댓글"을 남길 수 있다고 가정해 보겠습니다. 다형적 관계를 활용하면, 하나의 `comments` 테이블에서 게시글과 비디오의 모든 댓글을 저장할 수 있습니다. 아래는 필요한 테이블 구조 예시입니다.

```
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
이 연관관계를 구축하기 위한 모델 정의는 다음과 같습니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Comment extends Model
{
    /**
     * Get the parent commentable model (post or video).
     */
    public function commentable()
    {
        return $this->morphTo();
    }
}

class Post extends Model
{
    /**
     * Get all of the post's comments.
     */
    public function comments()
    {
        return $this->morphMany(Comment::class, 'commentable');
    }
}

class Video extends Model
{
    /**
     * Get all of the video's comments.
     */
    public function comments()
    {
        return $this->morphMany(Comment::class, 'commentable');
    }
}
```

<a name="one-to-many-polymorphic-retrieving-the-relationship"></a>
<!-- #### Retrieving The Relationship -->
#### Retrieving The Relationship

<!-- Once your database table and models are defined, you may access the relationships via your model's dynamic relationship properties. For example, to access all of the comments for a post, we can use the `comments` dynamic property: -->
테이블과 모델을 정의했다면, 모델의 동적 연관관계 프로퍼티를 통해 쉽게 데이터를 접근할 수 있습니다. 예를 들어, 게시글의 모든 댓글을 조회하려면 `comments` 동적 프로퍼티를 사용할 수 있습니다.

```
use App\Models\Post;

$post = Post::find(1);

foreach ($post->comments as $comment) {
    //
}
```

<!-- You may also retrieve the parent of a polymorphic child model by accessing the name of the method that performs the call to `morphTo`. In this case, that is the `commentable` method on the `Comment` model. So, we will access that method as a dynamic relationship property in order to access the comment's parent model: -->
또한, 다형적 자식 모델의 부모를 조회할 때도, `morphTo`를 호출하는 메서드명을 동적 연관관계 프로퍼티로 접근하면 됩니다. 이 예시에서는 `Comment` 모델의 `commentable`을 사용합니다.

```
use App\Models\Comment;

$comment = Comment::find(1);

$commentable = $comment->commentable;
```

<!-- The `commentable` relation on the `Comment` model will return either a `Post` or `Video` instance, depending on which type of model is the comment's parent. -->
`Comment` 모델의 `commentable` 연관관계는 해당 댓글이 속한 부모가 `Post`인지 `Video`인지에 따라 각각의 인스턴스를 반환합니다.

<a name="one-of-many-polymorphic-relations"></a>
<!-- ### One Of Many (Polymorphic) -->
### One Of Many (Polymorphic)

<!-- Sometimes a model may have many related models, yet you want to easily retrieve the "latest" or "oldest" related model of the relationship. For example, a `User` model may be related to many `Image` models, but you want to define a convenient way to interact with the most recent image the user has uploaded. You may accomplish this using the `morphOne` relationship type combined with the `ofMany` methods: -->
모델이 여러 관련 모델을 가질 수 있지만, 이 중에서 "최신" 또는 "가장 오래된" 연관된 모델을 간편하게 조회하고 싶을 때가 있습니다. 예를 들어, `User` 모델이 여러 개의 `Image` 모델과 연관되어 있을 때, 사용자가 마지막에 업로드한 이미지만을 편리하게 가져오고 싶을 수 있습니다. 이런 기능은 `morphOne` 관계와 `ofMany` 관련 메서드를 조합하여 구현할 수 있습니다.

```php
/**
 * Get the user's most recent image.
 */
public function latestImage()
{
    return $this->morphOne(Image::class, 'imageable')->latestOfMany();
}
```

<!-- Likewise, you may define a method to retrieve the "oldest", or first, related model of a relationship: -->
마찬가지로, 가장 오래된 이미지(최초 업로드 이미지 등)를 조회하는 메서드도 아래와 같이 정의할 수 있습니다.

```php
/**
 * Get the user's oldest image.
 */
public function oldestImage()
{
    return $this->morphOne(Image::class, 'imageable')->oldestOfMany();
}
```

<!-- By default, the `latestOfMany` and `oldestOfMany` methods will retrieve the latest or oldest related model based on the model's primary key, which must be sortable. However, sometimes you may wish to retrieve a single model from a larger relationship using a different sorting criteria. -->
`latestOfMany`와 `oldestOfMany` 메서드는 기본적으로 관련 모델의 기본 키(정렬이 가능한 값)를 기준으로 가장 최신 또는 가장 오래된 인스턴스를 조회합니다. 하지만, 더 복잡한 조건으로 단 하나의 연관 모델을 선택해서 가져오고 싶을 수도 있습니다.

<!-- For example, using the `ofMany` method, you may retrieve the user's most "liked" image. The `ofMany` method accepts the sortable column as its first argument and which aggregate function (`min` or `max`) to apply when querying for the related model: -->
예를 들어, `ofMany` 메서드를 사용하면 사용자의 "가장 많은 좋아요를 받은" 이미지를 조회할 수 있습니다. `ofMany`의 첫 번째 인수로 정렬 기준이 될 컬럼명을, 두 번째 인수로 집계 함수(`min` 또는 `max`)를 지정합니다.

```php
/**
 * Get the user's most popular image.
 */
public function bestImage()
{
    return $this->morphOne(Image::class, 'imageable')->ofMany('likes', 'max');
}
```

> [!TIP]
> 더 복잡한 "one of many" 연관관계도 구현할 수 있습니다. 자세한 내용은 [has one of many documentation](#advanced-has-one-of-many-relationships)를 참고하시기 바랍니다.

<a name="many-to-many-polymorphic-relations"></a>
<!-- ### Many To Many (Polymorphic) -->
### Many To Many (Polymorphic)

<a name="many-to-many-polymorphic-table-structure"></a>
<!-- #### Table Structure -->
#### Table Structure

<!-- Many-to-many polymorphic relations are slightly more complicated than "morph one" and "morph many" relationships. For example, a `Post` model and `Video` model could share a polymorphic relation to a `Tag` model. Using a many-to-many polymorphic relation in this situation would allow your application to have a single table of unique tags that may be associated with posts or videos. First, let's examine the table structure required to build this relationship: -->
다대다(polymorphic) 관계는 "morph one" 및 "morph many" 관계보다 조금 더 복잡합니다. 예를 들어, `Post` 모델과 `Video` 모델이 `Tag` 모델과 다형성 다대다 관계를 가질 수 있습니다. 이런 경우 하나의 태그 테이블을 통해 게시글과 비디오 모두에 고유한 태그를 연결할 수 있습니다. 아래는 이 관계를 구현하기에 필요한 테이블 구조입니다.

```
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

> [!TIP]
> 다형 다대다 관계 예제를 본격적으로 다루기 전에, 일반적인 [many-to-many relationships](#many-to-many)를 먼저 학습하면 더욱 이해가 잘 됩니다.

<a name="many-to-many-polymorphic-model-structure"></a>
<!-- #### Model Structure -->
#### Model Structure

<!-- Next, we're ready to define the relationships on the models. The `Post` and `Video` models will both contain a `tags` method that calls the `morphToMany` method provided by the base Eloquent model class. -->
이제 각 모델에 연관관계를 정의할 차례입니다. `Post`와 `Video` 모델 모두 기본 Eloquent 모델 클래스에서 제공하는 `morphToMany` 메서드를 호출하는 `tags` 메서드를 포함해야 합니다.

<!-- The `morphToMany` method accepts the name of the related model as well as the "relationship name". Based on the name we assigned to our intermediate table name and the keys it contains, we will refer to the relationship as "taggable": -->
`morphToMany` 메서드는 연관된 모델명과 "연관관계 이름"을 인수로 받습니다. 중간 테이블의 이름과 키를 기준으로 이 연관관계에서는 "taggable"이라는 이름을 사용하게 됩니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Post extends Model
{
    /**
     * Get all of the tags for the post.
     */
    public function tags()
    {
        return $this->morphToMany(Tag::class, 'taggable');
    }
}
```

<a name="many-to-many-polymorphic-defining-the-inverse-of-the-relationship"></a>
<!-- #### Defining The Inverse Of The Relationship -->
#### Defining The Inverse Of The Relationship

<!-- Next, on the `Tag` model, you should define a method for each of its possible parent models. So, in this example, we will define a `posts` method and a `videos` method. Both of these methods should return the result of the `morphedByMany` method. -->
이제 `Tag` 모델에 각 부모 모델에 해당하는 메서드를 각각 정의해야 합니다. 즉, 이 예시에서는 `posts`와 `videos` 메서드를 만들어야 하며, 두 메서드 모두 `morphedByMany` 메서드의 반환값을 리턴해야 합니다.

<!-- The `morphedByMany` method accepts the name of the related model as well as the "relationship name". Based on the name we assigned to our intermediate table name and the keys it contains, we will refer to the relationship as "taggable": -->
`morphedByMany`는 연관된 모델명과 "연관관계 이름"을 인수로 받습니다. 중간 테이블 및 관련 키에서 이미 사용했던 "taggable"이라는 이름을 그대로 사용합니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Tag extends Model
{
    /**
     * Get all of the posts that are assigned this tag.
     */
    public function posts()
    {
        return $this->morphedByMany(Post::class, 'taggable');
    }

    /**
     * Get all of the videos that are assigned this tag.
     */
    public function videos()
    {
        return $this->morphedByMany(Video::class, 'taggable');
    }
}
```

<a name="many-to-many-polymorphic-retrieving-the-relationship"></a>

<!-- #### Retrieving The Relationship -->
#### Retrieving The Relationship

<!-- Once your database table and models are defined, you may access the relationships via your models. For example, to access all of the tags for a post, you may use the `tags` dynamic relationship property: -->
데이터베이스 테이블과 모델을 정의한 이후에는 모델을 통해 손쉽게 관계 데이터를 조회할 수 있습니다. 예를 들어, 게시글에 연결된 모든 태그를 가져오려면 `tags` 동적 관계 속성을 사용할 수 있습니다.

```
use App\Models\Post;

$post = Post::find(1);

foreach ($post->tags as $tag) {
    //
}
```

<!-- You may retrieve the parent of a polymorphic relation from the polymorphic child model by accessing the name of the method that performs the call to `morphedByMany`. In this case, that is the `posts` or `videos` methods on the `Tag` model: -->
다형성 관계의 부모를 조회하려면, 다형성 자식 모델에서 `morphedByMany`를 호출하는 메서드의 이름을 통해 접근할 수 있습니다. 이번 예시에서는 `Tag` 모델의 `posts` 또는 `videos` 메서드가 여기에 해당합니다.

```
use App\Models\Tag;

$tag = Tag::find(1);

foreach ($tag->posts as $post) {
    //
}

foreach ($tag->videos as $video) {
    //
}
```

<a name="custom-polymorphic-types"></a>
<!-- ### Custom Polymorphic Types -->
### Custom Polymorphic Types

<!-- By default, Laravel will use the fully qualified class name to store the "type" of the related model. For instance, given the one-to-many relationship example above where a `Comment` model may belong to a `Post` or a `Video` model, the default `commentable_type` would be either `App\Models\Post` or `App\Models\Video`, respectively. However, you may wish to decouple these values from your application's internal structure. -->
기본적으로 Laravel은 연관된 모델의 "타입" 정보를 저장할 때 완전히 한정된 클래스명을 사용합니다. 앞서 살펴본 일대다 다형성 관계에서 `Comment` 모델이 `Post` 또는 `Video` 모델에 속한다면, 기본적인 `commentable_type` 컬럼에는 각각 `App\Models\Post` 또는 `App\Models\Video` 값이 저장됩니다. 하지만, 이런 값들을 애플리케이션의 내부 구조와 분리하려고 할 수 있습니다.

<!-- For example, instead of using the model names as the "type", we may use simple strings such as `post` and `video`. By doing so, the polymorphic "type" column values in our database will remain valid even if the models are renamed: -->
예를 들어, 모델명을 타입으로 사용하는 대신 단순한 문자열 `post`, `video` 등으로도 지정할 수 있습니다. 이렇게 하면 나중에 모델명을 변경해도 데이터베이스의 다형성 타입 컬럼 값이 유효하게 유지됩니다.

```
use Illuminate\Database\Eloquent\Relations\Relation;

Relation::enforceMorphMap([
    'post' => 'App\Models\Post',
    'video' => 'App\Models\Video',
]);
```

<!-- You may call the `enforceMorphMap` method in the `boot` method of your `App\Providers\AppServiceProvider` class or create a separate service provider if you wish. -->
`enforceMorphMap` 메서드는 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 호출하거나, 별도의 서비스 프로바이더를 만들어 정의해도 됩니다.

<!-- You may determine the morph alias of a given model at runtime using the model's `getMorphClass` method. Conversely, you may determine the fully-qualified class name associated with a morph alias using the `Relation::getMorphedModel` method: -->
런타임에 특정 모델의 다형성 별칭(별칭, alias)을 확인하려면, 해당 모델의 `getMorphClass` 메서드를 사용할 수 있습니다. 반대로, 다형성 맵에 등록된 별칭으로부터 완전한 클래스명을 얻고 싶다면 `Relation::getMorphedModel` 메서드를 사용하면 됩니다.

```
use Illuminate\Database\Eloquent\Relations\Relation;

$alias = $post->getMorphClass();

$class = Relation::getMorphedModel($alias);
```

> [!NOTE]
> 기존 애플리케이션에 "morph map"을 추가할 때에는, 데이터베이스의 모든 다형성 `*_type` 컬럼 값(완전한 클래스명이 저장되어 있던 값들)을 반드시 맵에서 정의한 "별칭" 값으로 변경해주어야 합니다.

<a name="dynamic-relationships"></a>
<!-- ### Dynamic Relationships -->
### Dynamic Relationships

<!-- You may use the `resolveRelationUsing` method to define relations between Eloquent models at runtime. While not typically recommended for normal application development, this may occasionally be useful when developing Laravel packages. -->
`resolveRelationUsing` 메서드를 사용하면 Eloquent 모델 간의 관계를 런타임에 동적으로 정의할 수 있습니다. 일반적인 애플리케이션 개발에서는 주로 권장되지 않지만, Laravel 패키지 개발 등에서는 유용할 수 있습니다.

<!-- The `resolveRelationUsing` method accepts the desired relationship name as its first argument. The second argument passed to the method should be a closure that accepts the model instance and returns a valid Eloquent relationship definition. Typically, you should configure dynamic relationships within the boot method of a [service provider](/docs/8.x/providers): -->
`resolveRelationUsing`의 첫 번째 인수로 원하는 관계명을 지정하고, 두 번째 인수로는 모델 인스턴스를 받아 유효한 Eloquent 관계 정의를 반환하는 클로저를 전달해야 합니다. 보통 이런 동적 관계 정의는 [service provider](/docs/8.x/providers) 클래스의 boot 메서드에서 수행합니다.

```
use App\Models\Order;
use App\Models\Customer;

Order::resolveRelationUsing('customer', function ($orderModel) {
    return $orderModel->belongsTo(Customer::class, 'customer_id');
});
```

> [!NOTE]
> 동적 관계를 정의할 때는 Eloquent 관계 메서드에 키 이름을 명확하게 지정하는 것이 좋습니다.

<a name="querying-relations"></a>
<!-- ## Querying Relations -->
## Querying Relations

<!-- Since all Eloquent relationships are defined via methods, you may call those methods to obtain an instance of the relationship without actually executing a query to load the related models. In addition, all types of Eloquent relationships also serve as [query builders](/docs/8.x/queries), allowing you to continue to chain constraints onto the relationship query before finally executing the SQL query against your database. -->
모든 Eloquent 관계는 메서드로 정의하므로, 실제 쿼리를 실행하지 않고도 관계 인스턴스를 얻을 수 있습니다. 또한 모든 종류의 Eloquent 관계는 [query builders](/docs/8.x/queries)로 동작하므로, 데이터베이스에 최종적으로 쿼리를 실행하기 전까지 관계 쿼리에 다양한 조건을 메서드 체이닝 방식으로 추가할 수 있습니다.

<!-- For example, imagine a blog application in which a `User` model has many associated `Post` models: -->
예를 들어, 블로그 애플리케이션에서 `User` 모델이 여러 개의 `Post` 모델을 가지고 있다고 가정하겠습니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * Get all of the posts for the user.
     */
    public function posts()
    {
        return $this->hasMany(Post::class);
    }
}
```

<!-- You may query the `posts` relationship and add additional constraints to the relationship like so: -->
이제 다음과 같이 `posts` 관계에 쿼리 조건을 체이닝하여 추가할 수 있습니다.

```
use App\Models\User;

$user = User::find(1);

$user->posts()->where('active', 1)->get();
```

<!-- You are able to use any of the Laravel [query builder's](/docs/8.x/queries) methods on the relationship, so be sure to explore the query builder documentation to learn about all of the methods that are available to you. -->
Laravel의 [query builder's](/docs/8.x/queries) 메서드는 관계 쿼리에도 모두 사용할 수 있으니, 쿼리 빌더 문서를 확인해 다양한 메서드를 익히시기 바랍니다.

<a name="chaining-orwhere-clauses-after-relationships"></a>
<!-- #### Chaining `orWhere` Clauses After Relationships -->
#### Chaining `orWhere` Clauses After Relationships

<!-- As demonstrated in the example above, you are free to add additional constraints to relationships when querying them. However, use caution when chaining `orWhere` clauses onto a relationship, as the `orWhere` clauses will be logically grouped at the same level as the relationship constraint: -->
앞서 예제에서 보았듯이, 관계 쿼리에 조건을 자유롭게 추가할 수 있습니다. 하지만, 관계 쿼리에 `orWhere` 절을 체이닝할 때에는 주의가 필요합니다. `orWhere` 절은 관계의 기본 조건과 같은 수준에서 묶이기 때문입니다.

```
$user->posts()
        ->where('active', 1)
        ->orWhere('votes', '>=', 100)
        ->get();
```

<!-- The example above will generate the following SQL. As you can see, the `or` clause instructs the query to return _any_ user with greater than 100 votes. The query is no longer constrained to a specific user: -->
위의 코드가 생성하는 SQL 문을 보면, `or`절 때문에 "100표 이상 받은 모든 사용자(user_id와 관계없이)"의 게시글도 결과에 포함되게 됩니다. 즉, 원래 특정 사용자에 한정되어야 할 쿼리 범위가 벗어나게 됩니다.

```sql
select *
from posts
where user_id = ? and active = 1 or votes >= 100
```

<!-- In most situations, you should use [logical groups](/docs/8.x/queries#logical-grouping) to group the conditional checks between parentheses: -->
대부분의 경우, 조건들을 괄호로 묶어서 [logical groups](/docs/8.x/queries#logical-grouping)을 활용해 별도로 묶어주는 것이 좋습니다.

```
use Illuminate\Database\Eloquent\Builder;

$user->posts()
        ->where(function (Builder $query) {
            return $query->where('active', 1)
                         ->orWhere('votes', '>=', 100);
        })
        ->get();
```

<!-- The example above will produce the following SQL. Note that the logical grouping has properly grouped the constraints and the query remains constrained to a specific user: -->
이 방식으로 생성되는 SQL은 아래와 같으며, 각 조건이 올바르게 그룹화되어 특정 사용자의 게시글로 제한됩니다.

```sql
select *
from posts
where user_id = ? and (active = 1 or votes >= 100)
```

<a name="relationship-methods-vs-dynamic-properties"></a>
<!-- ### Relationship Methods Vs. Dynamic Properties -->
### Relationship Methods Vs. Dynamic Properties

<!-- If you do not need to add additional constraints to an Eloquent relationship query, you may access the relationship as if it were a property. For example, continuing to use our `User` and `Post` example models, we may access all of a user's posts like so: -->
관계 쿼리에 별도의 제약 조건을 추가하지 않는다면, 관계를 마치 모델의 일반 속성처럼 접근할 수 있습니다. 앞서 살펴본 `User`와 `Post` 예제를 이어, 한 사용자의 모든 게시글에 접근하는 코드는 다음과 같습니다.

```
use App\Models\User;

$user = User::find(1);

foreach ($user->posts as $post) {
    //
}
```

<!-- Dynamic relationship properties perform "lazy loading", meaning they will only load their relationship data when you actually access them. Because of this, developers often use [eager loading](#eager-loading) to pre-load relationships they know will be accessed after loading the model. Eager loading provides a significant reduction in SQL queries that must be executed to load a model's relations. -->
동적 관계 속성은 "지연 로딩(레이지 로딩)" 방식으로 동작하므로, 실제로 속성에 접근할 때에만 관계 데이터가 로딩됩니다. 이 때문에, 개발자들은 보통 [eager loading](#eager-loading) 기능을 활용해 모델을 로딩할 때 미리 관계 데이터를 함께 불러와 SQL 쿼리 실행 횟수를 크게 줄입니다.

<a name="querying-relationship-existence"></a>
<!-- ### Querying Relationship Existence -->
### Querying Relationship Existence

<!-- When retrieving model records, you may wish to limit your results based on the existence of a relationship. For example, imagine you want to retrieve all blog posts that have at least one comment. To do so, you may pass the name of the relationship to the `has` and `orHas` methods: -->
모델 레코드를 조회할 때, 특정 관계의 존재 여부로 결과를 제한하고 싶을 수 있습니다. 예를 들어, 하나 이상의 댓글이 달린 블로그 게시글만 조회하고 싶을 때, `has` 또는 `orHas` 메서드에 관계명을 전달해 사용할 수 있습니다.

```
use App\Models\Post;

// Retrieve all posts that have at least one comment...
$posts = Post::has('comments')->get();
```

<!-- You may also specify an operator and count value to further customize the query: -->
연산자와 개수를 지정하면 더욱 세밀한 조건으로 결과를 조정할 수 있습니다.

```
// Retrieve all posts that have three or more comments...
$posts = Post::has('comments', '>=', 3)->get();
```

<!-- Nested `has` statements may be constructed using "dot" notation. For example, you may retrieve all posts that have at least one comment that has at least one image: -->
중첩된 `has` 조건문은 "점(dot) 표기법"을 활용해 손쉽게 작성할 수 있습니다. 예를 들어, 최소 한 개 이상의 이미지가 첨부된 댓글이 있는 모든 게시글을 조회할 수 있습니다.

```
// Retrieve posts that have at least one comment with images...
$posts = Post::has('comments.images')->get();
```

<!-- If you need even more power, you may use the `whereHas` and `orWhereHas` methods to define additional query constraints on your `has` queries, such as inspecting the content of a comment: -->
더 강력한 제약 조건이 필요하다면, `whereHas`와 `orWhereHas` 메서드를 사용해 `has` 쿼리에 추가적인 조건도 지정할 수 있습니다. 예를 들어 댓글의 내용을 검사하는 경우가 이에 해당합니다.

```
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

> [!NOTE]
> 현재 Eloquent는 데이터베이스 간의 관계 존재 여부 쿼리를 지원하지 않습니다. 반드시 같은 데이터베이스 내에 관계가 존재해야 합니다.

<a name="inline-relationship-existence-queries"></a>
<!-- #### Inline Relationship Existence Queries -->
#### Inline Relationship Existence Queries

<!-- If you would like to query for a relationship's existence with a single, simple where condition attached to the relationship query, you may find it more convenient to use the `whereRelation` and `whereMorphRelation` methods. For example, we may query for all posts that have unapproved comments: -->
관계 쿼리에 단일 where 조건을 곁들여 있고 싶을 때는 `whereRelation`과 `whereMorphRelation` 메서드를 활용하면 더 간결한 코드를 작성할 수 있습니다. 예를 들어, 승인되지 않은 댓글이 달린 게시글을 다음과 같이 조회할 수 있습니다.

```
use App\Models\Post;

$posts = Post::whereRelation('comments', 'is_approved', false)->get();
```

<!-- Of course, like calls to the query builder's `where` method, you may also specify an operator: -->
물론, 쿼리 빌더의 `where` 메서드처럼 연산자도 지정할 수 있습니다.

```
$posts = Post::whereRelation(
    'comments', 'created_at', '>=', now()->subHour()
)->get();
```

<a name="querying-relationship-absence"></a>
<!-- ### Querying Relationship Absence -->
### Querying Relationship Absence

<!-- When retrieving model records, you may wish to limit your results based on the absence of a relationship. For example, imagine you want to retrieve all blog posts that **don't** have any comments. To do so, you may pass the name of the relationship to the `doesntHave` and `orDoesntHave` methods: -->
모델 레코드를 조회할 때 특정 관계가 **존재하지 않는** 경우로 결과를 제한하고 싶을 때도 있습니다. 예를 들어, 댓글이 한 개도 없는 게시글만 조회하려면, `doesntHave` 또는 `orDoesntHave` 메서드에 관계명을 전달합니다.

```
use App\Models\Post;

$posts = Post::doesntHave('comments')->get();
```

<!-- If you need even more power, you may use the `whereDoesntHave` and `orWhereDoesntHave` methods to add additional query constraints to your `doesntHave` queries, such as inspecting the content of a comment: -->
더 정교한 제약 조건이 필요하다면 `whereDoesntHave`와 `orWhereDoesntHave` 메서드를 활용해 `doesntHave` 쿼리에 댓글의 내용 검사 같은 추가 제약을 줄 수 있습니다.

```
use Illuminate\Database\Eloquent\Builder;

$posts = Post::whereDoesntHave('comments', function (Builder $query) {
    $query->where('content', 'like', 'code%');
})->get();
```

<!-- You may use "dot" notation to execute a query against a nested relationship. For example, the following query will retrieve all posts that do not have comments; however, posts that have comments from authors that are not banned will be included in the results: -->
"점(dot) 표기법"을 사용하면 중첩 관계에서도 쿼리가 가능합니다. 아래 예시는 댓글이 없는 게시글을 조회하지만, "밴 처리되지 않은(banned=0) 작성자가 단 댓글"은 있는 게시글 또한 결과에 포함됩니다.

```
use Illuminate\Database\Eloquent\Builder;

$posts = Post::whereDoesntHave('comments.author', function (Builder $query) {
    $query->where('banned', 0);
})->get();
```

<a name="querying-morph-to-relationships"></a>
<!-- ### Querying Morph To Relationships -->
### Querying Morph To Relationships

<!-- To query the existence of "morph to" relationships, you may use the `whereHasMorph` and `whereDoesntHaveMorph` methods. These methods accept the name of the relationship as their first argument. Next, the methods accept the names of the related models that you wish to include in the query. Finally, you may provide a closure which customizes the relationship query: -->
"morph to" 관계에 대해 존재 쿼리를 작성하려면, `whereHasMorph`와 `whereDoesntHaveMorph` 메서드를 사용하면 됩니다. 이들 메서드의 첫 번째 인수는 관계명, 두 번째 인수는 쿼리에 포함하고자 하는 관련 모델명들이며, 마지막 인수로는 관계 쿼리를 추가로 커스터마이즈 할 수 있는 클로저를 전달할 수 있습니다.

```
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
경우에 따라서는 다형성 모델의 "타입"에 따라 쿼리 조건을 다르게 걸어야 할 수도 있습니다. 이때 `whereHasMorph`에 전달하는 클로저는 두 번째 인수로 `$type` 값을 받을 수 있으며, 이를 통해 빌드되는 쿼리 타입을 동적으로 분기할 수 있습니다.

```
use Illuminate\Database\Eloquent\Builder;

$comments = Comment::whereHasMorph(
    'commentable',
    [Post::class, Video::class],
    function (Builder $query, $type) {
        $column = $type === Post::class ? 'content' : 'title';

        $query->where($column, 'like', 'code%');
    }
)->get();
```

<a name="querying-all-morph-to-related-models"></a>
<!-- #### Querying All Related Models -->
#### Querying All Related Models

<!-- Instead of passing an array of possible polymorphic models, you may provide `*` as a wildcard value. This will instruct Laravel to retrieve all of the possible polymorphic types from the database. Laravel will execute an additional query in order to perform this operation: -->
특정 다형성 모델 배열을 전달하는 대신, `*`(애스터리스크)를 와일드카드로 넘길 수 있습니다. 이 경우 Laravel은 데이터베이스에서 존재하는 모든 다형성 타입을 조회하며, 이를 위해 별도의 쿼리가 추가로 실행됩니다.

```
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
관계에 속한 모델의 전체 개수를 가져오되, 실제 모델 전체를 로드하지 않고 싶을 수도 있습니다. 이럴 때는 `withCount` 메서드를 이용하세요. `withCount` 메서드는 결과 모델에 `{relation}_count` 형태의 속성을 추가해줍니다.

```
use App\Models\Post;

$posts = Post::withCount('comments')->get();

foreach ($posts as $post) {
    echo $post->comments_count;
}
```

<!-- By passing an array to the `withCount` method, you may add the "counts" for multiple relations as well as add additional constraints to the queries: -->
`withCount`에 배열을 전달하면 여러 관계의 개수를 한 번에 가져오거나, 추가 쿼리 조건도 걸 수 있습니다.

```
use Illuminate\Database\Eloquent\Builder;

$posts = Post::withCount(['votes', 'comments' => function (Builder $query) {
    $query->where('content', 'like', 'code%');
}])->get();

echo $posts[0]->votes_count;
echo $posts[0]->comments_count;
```

<!-- You may also alias the relationship count result, allowing multiple counts on the same relationship: -->
또한, 관계 카운트를 별칭(alias)으로 지정할 수도 있어, 동일한 관계에 대해 여러 개의 카운트를 구할 수 있습니다.

```
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
`loadCount` 메서드를 사용하면, 부모 모델을 이미 조회한 후에 관계 개수만 별도로 추가 로딩할 수 있습니다.

```
$book = Book::first();

$book->loadCount('genres');
```

<!-- If you need to set additional query constraints on the count query, you may pass an array keyed by the relationships you wish to count. The array values should be closures which receive the query builder instance: -->
카운트 쿼리에 추가 제약 조건을 지정하고 싶으면, 배열의 키에 관계명을, 값으로 쿼리 빌더를 받는 클로저를 넘겨주면 됩니다.

```
$book->loadCount(['reviews' => function ($query) {
    $query->where('rating', 5);
}])
```

<a name="relationship-counting-and-custom-select-statements"></a>
<!-- #### Relationship Counting & Custom Select Statements -->
#### Relationship Counting & Custom Select Statements

<!-- If you're combining `withCount` with a `select` statement, ensure that you call `withCount` after the `select` method: -->
`withCount`를 `select` 구문과 함께 쓸 때는 반드시 `select` 메서드 이후에 `withCount`를 호출해야 합니다.

```
$posts = Post::select(['title', 'body'])
                ->withCount('comments')
                ->get();
```

<a name="other-aggregate-functions"></a>
<!-- ### Other Aggregate Functions -->
### Other Aggregate Functions

<!-- In addition to the `withCount` method, Eloquent provides `withMin`, `withMax`, `withAvg`, `withSum`, and `withExists` methods. These methods will place a `{relation}_{function}_{column}` attribute on your resulting models: -->
`withCount` 외에도, Eloquent는 `withMin`, `withMax`, `withAvg`, `withSum`, `withExists` 등의 메서드를 제공합니다. 이 메서드들은 `{relation}_{function}_{column}` 형태의 속성을 결과 모델에 추가합니다.

```
use App\Models\Post;

$posts = Post::withSum('comments', 'votes')->get();

foreach ($posts as $post) {
    echo $post->comments_sum_votes;
}
```

<!-- If you wish to access the result of the aggregate function using another name, you may specify your own alias: -->
집계 함수 결과를 다른 이름으로 접근하고 싶을 경우, 별칭을 사용할 수 있습니다.

```
$posts = Post::withSum('comments as total_comments', 'votes')->get();

foreach ($posts as $post) {
    echo $post->total_comments;
}
```

<!-- Like the `loadCount` method, deferred versions of these methods are also available. These additional aggregate operations may be performed on Eloquent models that have already been retrieved: -->
`loadCount` 처럼, 이렇게 집계된 정보를 조회 후에 별도로 로드할 수도 있습니다.

```
$post = Post::first();

$post->loadSum('comments', 'votes');
```

<!-- If you're combining these aggregate methods with a `select` statement, ensure that you call the aggregate methods after the `select` method: -->
만약 이러한 집계 메서드들을 `select`와 조합하고자 한다면, 역시 `select` 메서드 이후에 집계 메서드를 호출해야 합니다.

```
$posts = Post::select(['title', 'body'])
                ->withExists('comments')
                ->get();
```

<a name="counting-related-models-on-morph-to-relationships"></a>
<!-- ### Counting Related Models On Morph To Relationships -->
### Counting Related Models On Morph To Relationships

<!-- If you would like to eager load a "morph to" relationship, as well as related model counts for the various entities that may be returned by that relationship, you may utilize the `with` method in combination with the `morphTo` relationship's `morphWithCount` method. -->
"morph to" 관계뿐만 아니라 각 관계가 반환할 수 있는 여러 엔티티의 카운트도 즉시 로딩하여 보고 싶을 때는, `with`와 `morphTo` 관계의 `morphWithCount` 메서드를 조합하면 됩니다.

<!-- In this example, let's assume that `Photo` and `Post` models may create `ActivityFeed` models. We will assume the `ActivityFeed` model defines a "morph to" relationship named `parentable` that allows us to retrieve the parent `Photo` or `Post` model for a given `ActivityFeed` instance. Additionally, let's assume that `Photo` models "have many" `Tag` models and `Post` models "have many" `Comment` models. -->
예를 들어, `Photo`, `Post` 모델이 각각 `ActivityFeed` 모델을 만들 수 있다고 합시다. `ActivityFeed` 모델에는 특정 `ActivityFeed` 인스턴스의 부모 `Photo` 또는 `Post` 모델에 접근할 수 있는 `parentable` "morph to" 관계가 있습니다. 추가적으로, `Photo` 모델은 여러 `Tag`와, `Post` 모델은 여러 `Comment`와 각각 연관 관계를 맺고 있다고 가정합니다.

<!-- Now, let's imagine we want to retrieve `ActivityFeed` instances and eager load the `parentable` parent models for each `ActivityFeed` instance. In addition, we want to retrieve the number of tags that are associated with each parent photo and the number of comments that are associated with each parent post: -->
이렇게 설정된 경우, `ActivityFeed` 인스턴스를 조회하면서 각 `ActivityFeed` 인스턴스의 부모 `parentable` 모델을 즉시 로딩하고, 각 부모마다 연결된 태그나 댓글 개수까지 함께 조회하려면 다음과 같이 하면 됩니다.

```
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
이미 여러 개의 `ActivityFeed` 모델을 먼저 조회했다면, 나중에 각 `parentable` 부모 모델의 하위 관계 개수를 지연 로딩 방식으로 가져올 수도 있습니다. 이때는 `loadMorphCount` 메서드를 사용하면 됩니다.

```
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
Eloquent 관계에 속성처럼 접근하면 연관된 데이터는 "지연 로딩"됩니다. 즉, 실제로 해당 속성에 접근할 때 쿼리가 발생합니다. 반면, Eloquent는 부모 모델을 쿼리할 때 특정 관계를 "즉시 로딩(eager loading)"할 수 있는 기능도 지원합니다. 즉시 로딩을 활용하면 이른바 "N + 1" 쿼리 문제를 해결할 수 있습니다. 이 문제를 설명하기 위해, 한 `Book` 모델이 `Author` 모델에 "belongs to" 관계를 맺고 있다고 가정해 보겠습니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Book extends Model
{
    /**
     * Get the author that wrote the book.
     */
    public function author()
    {
        return $this->belongsTo(Author::class);
    }
}
```

<!-- Now, let's retrieve all books and their authors: -->
이제 모든 책과 각 책의 저자를 조회하는 코드를 작성해 보겠습니다.

```
use App\Models\Book;

$books = Book::all();

foreach ($books as $book) {
    echo $book->author->name;
}
```

<!-- This loop will execute one query to retrieve all of the books within the database table, then another query for each book in order to retrieve the book's author. So, if we have 25 books, the code above would run 26 queries: one for the original book, and 25 additional queries to retrieve the author of each book. -->
이 루프에서는 데이터베이스에서 책 목록을 한 번 조회하고, 각 책마다 추가로 저자 정보를 조회하기 위해 반복적으로 쿼리가 실행됩니다. 만약 책이 25권이라면, 총 26번(책 전체 1번 + 책마다 저자 25번) 쿼리가 실행됩니다.

<!-- Thankfully, we can use eager loading to reduce this operation to just two queries. When building a query, you may specify which relationships should be eager loaded using the `with` method: -->
이때 "즉시 로딩"을 활용하면 이 작업을 단 두 번의 쿼리로 줄일 수 있습니다. 쿼리를 작성할 때 `with` 메서드를 사용해 관계를 명시적으로 즉시 로딩할 수 있습니다.

```
$books = Book::with('author')->get();

foreach ($books as $book) {
    echo $book->author->name;
}
```

<!-- For this operation, only two queries will be executed - one query to retrieve all of the books and one query to retrieve all of the authors for all of the books: -->
이렇게 하면 실제로 실행되는 쿼리는 두 번뿐입니다. 한 번은 모든 책을, 한 번은 해당하는 저자들을 조회합니다.

```sql
select * from books

select * from authors where id in (1, 2, 3, 4, 5, ...)
```

<a name="eager-loading-multiple-relationships"></a>
<!-- #### Eager Loading Multiple Relationships -->
#### Eager Loading Multiple Relationships

<!-- Sometimes you may need to eager load several different relationships. To do so, just pass an array of relationships to the `with` method: -->
여러 관계를 한 번에 즉시 로딩하려면, `with` 메서드에 관계명을 배열로 넘기면 됩니다.

```
$books = Book::with(['author', 'publisher'])->get();
```

<a name="nested-eager-loading"></a>
<!-- #### Nested Eager Loading -->
#### Nested Eager Loading

<!-- To eager load a relationship's relationships, you may use "dot" syntax. For example, let's eager load all of the book's authors and all of the author's personal contacts: -->
관계의 또 다른 관계까지 즉시 로딩하고 싶을 때는 "점(dot) 표기법"을 활용할 수 있습니다. 예를 들어, 모든 책의 저자와, 저자의 연락처까지 즉시 로딩하려면 다음과 같이 작성합니다.

```
$books = Book::with('author.contacts')->get();
```

<a name="nested-eager-loading-morphto-relationships"></a>
<!-- #### Nested Eager Loading `morphTo` Relationships -->
#### Nested Eager Loading `morphTo` Relationships

<!-- If you would like to eager load a `morphTo` relationship, as well as nested relationships on the various entities that may be returned by that relationship, you may use the `with` method in combination with the `morphTo` relationship's `morphWith` method. To help illustrate this method, let's consider the following model: -->
`morphTo` 관계와, 해당 관계가 반환할 수 있는 다양한 엔티티의 추가 관계까지 함께 즉시 로딩하려면, `with`와 `morphTo` 관계의 `morphWith` 메서드를 결합해서 사용할 수 있습니다. 다음 예시를 참고하세요.

```
<?php

use Illuminate\Database\Eloquent\Model;

class ActivityFeed extends Model
{
    /**
     * Get the parent of the activity feed record.
     */
    public function parentable()
    {
        return $this->morphTo();
    }
}
```

<!-- In this example, let's assume `Event`, `Photo`, and `Post` models may create `ActivityFeed` models. Additionally, let's assume that `Event` models belong to a `Calendar` model, `Photo` models are associated with `Tag` models, and `Post` models belong to an `Author` model. -->
이 예시에서 `Event`, `Photo`, `Post` 모델이 `ActivityFeed` 모델을 생성할 수 있다고 가정합니다. 또한 `Event` 모델은 `Calendar`와, `Photo`는 `Tag`와, `Post`는 `Author`와 각각 연결되어 있습니다.

<!-- Using these model definitions and relationships, we may retrieve `ActivityFeed` model instances and eager load all `parentable` models and their respective nested relationships: -->
이런 모델/관계 구성을 한다면, 아래 코드처럼 `ActivityFeed` 모델을 조회하면서 각각의 `parentable` 모델과, 해당 부모 모델의 중첩 관계까지 한 번에 즉시 로딩할 수 있습니다.

```
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
연관관계를 통해 데이터를 불러올 때, 항상 모든 컬럼이 필요한 것은 아닙니다. 이런 경우, Eloquent에서는 연관관계에서 어떤 컬럼만 조회할지 명시적으로 지정할 수 있습니다.

```
$books = Book::with('author:id,name,book_id')->get();
```

> [!NOTE]
> 이 기능을 사용할 때는 반드시 `id` 컬럼과 적절한 외래키 컬럼을 컬럼 목록에 포함시켜야 합니다.

<a name="eager-loading-by-default"></a>
<!-- #### Eager Loading By Default -->
#### Eager Loading By Default

<!-- Sometimes you might want to always load some relationships when retrieving a model. To accomplish this, you may define a `$with` property on the model: -->
모델을 조회할 때마다 항상 특정 연관관계를 로드하고 싶을 때가 있습니다. 이럴 때는 모델에 `$with` 속성을 정의하면 됩니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

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
    public function author()
    {
        return $this->belongsTo(Author::class);
    }

    /**
     * Get the genre of the book.
     */
    public function genre()
    {
        return $this->belongsTo(Genre::class);
    }
}
```

<!-- If you would like to remove an item from the `$with` property for a single query, you may use the `without` method: -->
단일 쿼리에서 `$with` 속성에 지정된 항목을 제외하고 싶다면 `without` 메서드를 사용할 수 있습니다.

```
$books = Book::without('author')->get();
```

<!-- If you would like to override all items within the `$with` property for a single query, you may use the `withOnly` method: -->
단일 쿼리에서 `$with`에 지정된 모든 항목을 원하는 값으로 다 덮어쓰고 싶으면 `withOnly` 메서드를 사용합니다.

```
$books = Book::withOnly('genre')->get();
```

<a name="constraining-eager-loads"></a>
<!-- ### Constraining Eager Loads -->
### Constraining Eager Loads

<!-- Sometimes you may wish to eager load a relationship but also specify additional query conditions for the eager loading query. You can accomplish this by passing an array of relationships to the `with` method where the array key is a relationship name and the array value is a closure that adds additional constraints to the eager loading query: -->
연관관계를 eager load 하면서 동시에 해당 쿼리에 추가 조건을 걸고 싶을 수도 있습니다. 이럴 때에는 `with` 메서드에 배열을 전달하고, 배열의 키는 연관관계 이름, 값은 조건을 추가하는 클로저로 작성할 수 있습니다.

```
use App\Models\User;

$users = User::with(['posts' => function ($query) {
    $query->where('title', 'like', '%code%');
}])->get();
```

<!-- In this example, Eloquent will only eager load posts where the post's `title` column contains the word `code`. You may call other [query builder](/docs/8.x/queries) methods to further customize the eager loading operation: -->
이 예시에서는, 게시글의 `title` 컬럼에 `code`라는 단어가 포함된 게시글만 eager load 하게 됩니다. 또한, [query builder](/docs/8.x/queries)의 다른 메서드들을 활용해 eager loading 쿼리를 원하는 대로 커스터마이즈할 수 있습니다.

```
$users = User::with(['posts' => function ($query) {
    $query->orderBy('created_at', 'desc');
}])->get();
```

> [!NOTE]
> `limit`과 `take` 쿼리 빌더 메서드는 eager load 제약 조건에서 사용할 수 없습니다.

<a name="constraining-eager-loading-of-morph-to-relationships"></a>
<!-- #### Constraining Eager Loading Of `morphTo` Relationships -->
#### Constraining Eager Loading Of `morphTo` Relationships

<!-- If you are eager loading a `morphTo` relationship, Eloquent will run multiple queries to fetch each type of related model. You may add additional constraints to each of these queries using the `MorphTo` relation's `constrain` method: -->
`morphTo` 연관관계를 eager load 할 때는, Eloquent가 각 관련된 모델별로 여러 쿼리를 실행합니다. 이 경우 각 쿼리에 제약 조건을 추가하려면, `MorphTo` 관계의 `constrain` 메서드를 이용할 수 있습니다:

```
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Relations\MorphTo;

$comments = Comment::with(['commentable' => function (MorphTo $morphTo) {
    $morphTo->constrain([
        Post::class => function (Builder $query) {
            $query->whereNull('hidden_at');
        },
        Video::class => function (Builder $query) {
            $query->where('type', 'educational');
        },
    ]);
}])->get();
```

<!-- In this example, Eloquent will only eager load posts that have not been hidden and videos have a `type` value of "educational". -->
위 예시에서 Eloquent는 숨겨지지 않은(Post의 경우) 게시글과, `type` 값이 "educational"인 비디오만 eager load 하게 됩니다.

<a name="lazy-eager-loading"></a>
<!-- ### Lazy Eager Loading -->
### Lazy Eager Loading

<!-- Sometimes you may need to eager load a relationship after the parent model has already been retrieved. For example, this may be useful if you need to dynamically decide whether to load related models: -->
간혹 상위(부모) 모델을 이미 조회한 뒤에 연관관계의 eager load가 필요한 경우가 있습니다. 예를 들어, 관련 모델을 로드할지 동적으로 결정해야 할 때 이런 방식이 유용합니다.

```
use App\Models\Book;

$books = Book::all();

if ($someCondition) {
    $books->load('author', 'publisher');
}
```

<!-- If you need to set additional query constraints on the eager loading query, you may pass an array keyed by the relationships you wish to load. The array values should be closure instances which receive the query instance: -->
eager load 쿼리에 조건을 추가해야 한다면, 로드할 연관관계를 키로, 클로저를 값으로 가지는 배열을 전달할 수 있습니다.

```
$author->load(['books' => function ($query) {
    $query->orderBy('published_date', 'asc');
}]);
```

<!-- To load a relationship only when it has not already been loaded, use the `loadMissing` method: -->
이미 로드되지 않은 관계만 로드하고자 한다면 `loadMissing` 메서드를 사용하세요.

```
$book->loadMissing('author');
```

<a name="nested-lazy-eager-loading-morphto"></a>
<!-- #### Nested Lazy Eager Loading & `morphTo` -->
#### Nested Lazy Eager Loading & `morphTo`

<!-- If you would like to eager load a `morphTo` relationship, as well as nested relationships on the various entities that may be returned by that relationship, you may use the `loadMorph` method. -->
`morphTo` 연관관계뿐만 아니라, 그 안에 등장할 수 있는 다양한 엔티티의 중첩 관계까지 eager load 하고 싶다면 `loadMorph` 메서드를 사용할 수 있습니다.

<!-- This method accepts the name of the `morphTo` relationship as its first argument, and an array of model / relationship pairs as its second argument. To help illustrate this method, let's consider the following model: -->
이 메서드는 첫 번째 인자로 `morphTo` 관계의 이름을, 두 번째 인자로 모델 및 해당 연관관계 목록의 배열을 받습니다. 아래 예시를 참고하세요.

```
<?php

use Illuminate\Database\Eloquent\Model;

class ActivityFeed extends Model
{
    /**
     * Get the parent of the activity feed record.
     */
    public function parentable()
    {
        return $this->morphTo();
    }
}
```

<!-- In this example, let's assume `Event`, `Photo`, and `Post` models may create `ActivityFeed` models. Additionally, let's assume that `Event` models belong to a `Calendar` model, `Photo` models are associated with `Tag` models, and `Post` models belong to an `Author` model. -->
여기서 예를 들어, `Event`, `Photo`, `Post` 모델들이 모두 `ActivityFeed` 모델을 생성할 수 있다고 가정합니다. 또한 `Event` 모델은 `Calendar` 모델과, `Photo` 모델은 `Tag` 모델과, `Post`는 `Author` 모델과 각각 연관되어 있다고 하겠습니다.

<!-- Using these model definitions and relationships, we may retrieve `ActivityFeed` model instances and eager load all `parentable` models and their respective nested relationships: -->
이런 모델/관계 구성을 바탕으로, 모든 `ActivityFeed` 모델 인스턴스를 조회하면서 각각의 `parentable` 모델과 그에 해당하는 중첩 관계까지 즉시 로딩할 수 있습니다.

```
$activities = ActivityFeed::with('parentable')
    ->get()
    ->loadMorph('parentable', [
        Event::class => ['calendar'],
        Photo::class => ['tags'],
        Post::class => ['author'],
    ]);
```

<a name="preventing-lazy-loading"></a>
<!-- ### Preventing Lazy Loading -->
### Preventing Lazy Loading

<!-- As previously discussed, eager loading relationships can often provide significant performance benefits to your application. Therefore, if you would like, you may instruct Laravel to always prevent the lazy loading of relationships. To accomplish this, you may invoke the `preventLazyLoading` method offered by the base Eloquent model class. Typically, you should call this method within the `boot` method of your application's `AppServiceProvider` class. -->
앞서 다룬 것처럼, eager loading을 적극적으로 활용하면 애플리케이션의 성능을 크게 높일 수 있습니다. 그래서 Laravel에서는 관계의 lazy loading을 항상 방지하도록 설정할 수 있습니다. 이를 위해 Eloquent 기본 모델 클래스의 `preventLazyLoading` 메서드를 사용합니다. 보통 이 코드는 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드에서 호출하는 것이 일반적입니다.

<!-- The `preventLazyLoading` method accepts an optional boolean argument that indicates if lazy loading should be prevented. For example, you may wish to only disable lazy loading in non-production environments so that your production environment will continue to function normally even if a lazy loaded relationship is accidentally present in production code: -->
`preventLazyLoading` 메서드는 lazy loading을 방지할지 여부를 나타내는 (불리언) 인자를 선택적으로 받습니다. 예를 들어, 프로덕션 환경이 아닐 때만 lazy loading을 막고 싶을 수도 있습니다. 이런 경우에도 프로덕션 환경에서는 기존 코드가 영향을 받지 않도록 처리할 수 있습니다.

```php
use Illuminate\Database\Eloquent\Model;

/**
 * Bootstrap any application services.
 *
 * @return void
 */
public function boot()
{
    Model::preventLazyLoading(! $this->app->isProduction());
}
```

<!-- After preventing lazy loading, Eloquent will throw a `Illuminate\Database\LazyLoadingViolationException` exception when your application attempts to lazy load any Eloquent relationship. -->
lazy loading을 방지하도록 설정하면, Eloquent가 관계를 lazy load 하려고 시도할 때마다 `Illuminate\Database\LazyLoadingViolationException` 예외가 발생하게 됩니다.

<!-- You may customize the behavior of lazy loading violations using the `handleLazyLoadingViolationsUsing` method. For example, using this method, you may instruct lazy loading violations to only be logged instead of interrupting the application's execution with exceptions: -->
lazy loading 위반 발생 시의 동작을 `handleLazyLoadingViolationsUsing` 메서드로 커스터마이즈할 수도 있습니다. 예를 들어, 예외를 발생시키는 대신 로그만 남기도록 하려면 아래와 같이 할 수 있습니다.

```php
Model::handleLazyLoadingViolationUsing(function ($model, $relation) {
    $class = get_class($model);

    info("Attempted to lazy load [{$relation}] on model [{$class}].");
});
```

<a name="inserting-and-updating-related-models"></a>
<!-- ## Inserting & Updating Related Models -->
## Inserting & Updating Related Models

<a name="the-save-method"></a>
<!-- ### The `save` Method -->
### The `save` Method

<!-- Eloquent provides convenient methods for adding new models to relationships. For example, perhaps you need to add a new comment to a post. Instead of manually setting the `post_id` attribute on the `Comment` model you may insert the comment using the relationship's `save` method: -->
Eloquent는 연관관계에 새 모델을 추가하기 위한 편리한 메서드를 제공합니다. 예를 들어, 기존 게시글에 새 댓글을 추가해야 한다고 할 때, 굳이 `Comment` 모델의 `post_id` 속성을 직접 지정하지 않아도, 연관관계의 `save` 메서드를 사용해서 댓글을 추가할 수 있습니다.

```
use App\Models\Comment;
use App\Models\Post;

$comment = new Comment(['message' => 'A new comment.']);

$post = Post::find(1);

$post->comments()->save($comment);
```

<!-- Note that we did not access the `comments` relationship as a dynamic property. Instead, we called the `comments` method to obtain an instance of the relationship. The `save` method will automatically add the appropriate `post_id` value to the new `Comment` model. -->
여기서는 `comments` 관계에 동적 프로퍼티로 접근하지 않고, `comments` 메서드를 호출해 관계 인스턴스를 얻은 점에 유의하세요. `save` 메서드는 새 `Comment` 모델의 `post_id` 값을 자동으로 채워줍니다.

<!-- If you need to save multiple related models, you may use the `saveMany` method: -->
여러 개의 연관 모델을 한 번에 저장하려면 `saveMany` 메서드를 사용할 수 있습니다.

```
$post = Post::find(1);

$post->comments()->saveMany([
    new Comment(['message' => 'A new comment.']),
    new Comment(['message' => 'Another new comment.']),
]);
```

<!-- The `save` and `saveMany` methods will persist the given model instances, but will not add the newly persisted models to any in-memory relationships that are already loaded onto the parent model. If you plan on accessing the relationship after using the `save` or `saveMany` methods, you may wish to use the `refresh` method to reload the model and its relationships: -->
`save`와 `saveMany` 메서드는 주어진 모델 인스턴스들을 데이터베이스에 저장하기는 하지만, 이미 로드된 부모 모델의 in-memory(메모리 상의) 관계에 새로 저장한 모델을 자동으로 추가하지는 않습니다. `save`나 `saveMany` 메서드를 사용한 뒤에 해당 관계에 접근할 계획이라면, `refresh`를 사용해 모델과 관계를 다시 로드하는 것이 좋습니다.

```
$post->comments()->save($comment);

$post->refresh();

// All comments, including the newly saved comment...
$post->comments;
```

<a name="the-push-method"></a>
<!-- #### Recursively Saving Models & Relationships -->
#### Recursively Saving Models & Relationships

<!-- If you would like to `save` your model and all of its associated relationships, you may use the `push` method. In this example, the `Post` model will be saved as well as its comments and the comment's authors: -->
모델과 그와 연결된 모든 연관 모델까지 한 번에 `save`하려면 `push` 메서드를 사용할 수 있습니다. 아래 예시에서, `Post` 모델뿐 아니라 그에 연결된 댓글, 그리고 각 댓글의 작성자까지 한 번에 저장됩니다.

```
$post = Post::find(1);

$post->comments[0]->message = 'Message';
$post->comments[0]->author->name = 'Author Name';

$post->push();
```

<a name="the-create-method"></a>
<!-- ### The `create` Method -->
### The `create` Method

<!-- In addition to the `save` and `saveMany` methods, you may also use the `create` method, which accepts an array of attributes, creates a model, and inserts it into the database. The difference between `save` and `create` is that `save` accepts a full Eloquent model instance while `create` accepts a plain PHP `array`. The newly created model will be returned by the `create` method: -->
`save`와 `saveMany` 외에도, 속성 배열을 전달해 새 모델을 생성하고 데이터베이스에 바로 저장하는 `create` 메서드를 사용할 수도 있습니다. `save`와 `create`의 차이는, `save`가 전체 Eloquent 모델 인스턴스를 받는 것과 달리 `create`는 일반 PHP `array`를 인자로 받는다는 점입니다. 새롭게 생성된 모델은 `create` 메서드의 반환값으로 받게 됩니다.

```
use App\Models\Post;

$post = Post::find(1);

$comment = $post->comments()->create([
    'message' => 'A new comment.',
]);
```

<!-- You may use the `createMany` method to create multiple related models: -->
`createMany` 메서드를 사용해 여러 연관 모델을 한 번에 생성할 수도 있습니다.

```
$post = Post::find(1);

$post->comments()->createMany([
    ['message' => 'A new comment.'],
    ['message' => 'Another new comment.'],
]);
```

<!-- You may also use the `findOrNew`, `firstOrNew`, `firstOrCreate`, and `updateOrCreate` methods to [create and update models on relationships](/docs/8.x/eloquent#upserts). -->
또한, `findOrNew`, `firstOrNew`, `firstOrCreate`, `updateOrCreate` 메서드로도 [create and update models on relationships](/docs/8.x/eloquent#upserts)할 수 있습니다.

> [!TIP]
> `create` 메서드를 사용하기 전에 [mass assignment](/docs/8.x/eloquent#mass-assignment) 관련 문서를 꼭 살펴보시기 바랍니다.

<a name="updating-belongs-to-relationships"></a>
<!-- ### Belongs To Relationships -->
### Belongs To Relationships

<!-- If you would like to assign a child model to a new parent model, you may use the `associate` method. In this example, the `User` model defines a `belongsTo` relationship to the `Account` model. This `associate` method will set the foreign key on the child model: -->
자식 모델에 새로운 부모 모델을 할당하고 싶다면 `associate` 메서드를 사용하면 됩니다. 아래 예시는 `User` 모델이 `Account` 모델과 `belongsTo` 관계를 가진 상황입니다. `associate` 메서드는 자식 모델에서 관계의 외래키를 자동으로 설정합니다.

```
use App\Models\Account;

$account = Account::find(10);

$user->account()->associate($account);

$user->save();
```

<!-- To remove a parent model from a child model, you may use the `dissociate` method. This method will set the relationship's foreign key to `null`: -->
자식 모델에서 부모 모델 연결을 해제하고 싶을 때는 `dissociate` 메서드를 사용하면 되며, 해당 관계의 외래키가 `null`로 설정됩니다.

```
$user->account()->dissociate();

$user->save();
```

<a name="updating-many-to-many-relationships"></a>
<!-- ### Many To Many Relationships -->
### Many To Many Relationships

<a name="attaching-detaching"></a>
<!-- #### Attaching / Detaching -->
#### Attaching / Detaching

<!-- Eloquent also provides methods to make working with many-to-many relationships more convenient. For example, let's imagine a user can have many roles and a role can have many users. You may use the `attach` method to attach a role to a user by inserting a record in the relationship's intermediate table: -->
Eloquent는 다대다 연관관계를 손쉽게 다룰 수 있는 여러 메서드를 제공합니다. 예를 들어, 한 사용자가 여러 역할(roles)을 가질 수 있고, 역할도 여러 사용자를 가질 수 있는 구조라면, 중간 테이블에 데이터를 기록하려면 `attach` 메서드를 사용할 수 있습니다.

```
use App\Models\User;

$user = User::find(1);

$user->roles()->attach($roleId);
```

<!-- When attaching a relationship to a model, you may also pass an array of additional data to be inserted into the intermediate table: -->
연관관계를 모델에 attach 할 때, 중간 테이블에 추가로 기록할 데이터를 배열 형태로 함께 전달할 수도 있습니다.

```
$user->roles()->attach($roleId, ['expires' => $expires]);
```

<!-- Sometimes it may be necessary to remove a role from a user. To remove a many-to-many relationship record, use the `detach` method. The `detach` method will delete the appropriate record out of the intermediate table; however, both models will remain in the database: -->
역할을 사용자로부터 분리(detach)하려면 `detach` 메서드를 사용합니다. `detach` 메서드는 해당 중간 테이블의 레코드만 삭제하며, 실제 모델 자체는 데이터베이스에 남아 있습니다.

```
// Detach a single role from the user...
$user->roles()->detach($roleId);

// Detach all roles from the user...
$user->roles()->detach();
```

<!-- For convenience, `attach` and `detach` also accept arrays of IDs as input: -->
참고로, `attach` 및 `detach`는 모두 ID 배열을 인자로 받는 것도 가능합니다.

```
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
다대다 관계의 연결을 만들 때는 `sync` 메서드를 사용할 수도 있습니다. `sync` 메서드는 중간 테이블에 둘 ID 배열을 받습니다. 배열에 없는 ID는 중간 테이블에서 제거됩니다. 즉, 이 작업이 끝나면 전달한 ID들만 중간 테이블에 남게 됩니다.

```
$user->roles()->sync([1, 2, 3]);
```

<!-- You may also pass additional intermediate table values with the IDs: -->
동기화 시 중간 테이블에 저장할 추가 데이터를 함께 전달할 수도 있습니다.

```
$user->roles()->sync([1 => ['expires' => true], 2, 3]);
```

<!-- If you would like to insert the same intermediate table values with each of the synced model IDs, you may use the `syncWithPivotValues` method: -->
모든 동기화된 ID에 동일한 중간 테이블 데이터를 기록하고 싶다면 `syncWithPivotValues` 메서드를 쓸 수 있습니다.

```
$user->roles()->syncWithPivotValues([1, 2, 3], ['active' => true]);
```

<!-- If you do not want to detach existing IDs that are missing from the given array, you may use the `syncWithoutDetaching` method: -->
주어진 배열에 포함되지 않은 기존 ID를 분리(detach)하지 않고 유지하고 싶다면, `syncWithoutDetaching`을 사용하세요.

```
$user->roles()->syncWithoutDetaching([1, 2, 3]);
```

<a name="toggling-associations"></a>
<!-- #### Toggling Associations -->
#### Toggling Associations

<!-- The many-to-many relationship also provides a `toggle` method which "toggles" the attachment status of the given related model IDs. If the given ID is currently attached, it will be detached. Likewise, if it is currently detached, it will be attached: -->
다대다 관계에는 주어진 관련 모델 ID의 연결 상태를 "토글"하는 `toggle` 메서드도 있습니다. 이 메서드는 전달된 ID가 이미 연결되어 있다면 분리하고, 연결되어 있지 않다면 새로 연결합니다.

```
$user->roles()->toggle([1, 2, 3]);
```

<a name="updating-a-record-on-the-intermediate-table"></a>
<!-- #### Updating A Record On The Intermediate Table -->
#### Updating A Record On The Intermediate Table

<!-- If you need to update an existing row in your relationship's intermediate table, you may use the `updateExistingPivot` method. This method accepts the intermediate record foreign key and an array of attributes to update: -->
이미 존재하는 중간 테이블의 레코드를 수정하려면, `updateExistingPivot` 메서드를 사용할 수 있습니다. 이 메서드는 중간 테이블의 외래키, 그리고 수정할 속성 배열을 받습니다.

```
$user = User::find(1);

$user->roles()->updateExistingPivot($roleId, [
    'active' => false,
]);
```

<a name="touching-parent-timestamps"></a>
<!-- ## Touching Parent Timestamps -->
## Touching Parent Timestamps

<!-- When a model defines a `belongsTo` or `belongsToMany` relationship to another model, such as a `Comment` which belongs to a `Post`, it is sometimes helpful to update the parent's timestamp when the child model is updated. -->
`belongsTo` 또는 `belongsToMany` 관계를 정의할 때(예: `Comment` → `Post`), 자식 모델이 수정될 때 부모 모델의 타임스탬프를 자동으로 업데이트하는 것이 유용할 때가 있습니다.

<!-- For example, when a `Comment` model is updated, you may want to automatically "touch" the `updated_at` timestamp of the owning `Post` so that it is set to the current date and time. To accomplish this, you may add a `touches` property to your child model containing the names of the relationships that should have their `updated_at` timestamps updated when the child model is updated: -->
예를 들어, `Comment` 모델을 수정하면 소유하고 있는 `Post`의 `updated_at` 값도 현재 시간으로 자동 업데이트하고 싶을 수 있습니다. 이런 경우, 자식 모델에 `touches` 속성을 추가하고, 자식 모델이 수정될 때 `updated_at` 타임스탬프를 함께 갱신할 관계 이름을 배열로 지정하면 됩니다.

```
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

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
    public function post()
    {
        return $this->belongsTo(Post::class);
    }
}
```

> [!NOTE]
> 부모 모델의 타임스탬프는 Eloquent의 `save` 메서드로 자식 모델이 수정될 때만 자동으로 업데이트됩니다.