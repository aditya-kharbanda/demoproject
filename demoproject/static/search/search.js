var searchUsers = (function() {
    function updateResults(users) {
        if (users.length === 0 ) {
            $('.collection-header').html('No Results!');
        } else {
            $('.collection-header').html(users.length + ' users found');
        }
        $('.collection-item').remove();
        for (var i = 0; i < users.length; i++) {
            var el = $('<li class="collection-item"/>');
            el.html(users[i].name);
            $('.collection').append(el);
        }
    }
    function getUsers() {
        $.ajax({
            url : '/account/search_users/',
            data: { name : $('#id_name').val() },
            type: 'GET',
            success: function(data, status, xhr) {
                updateResults(data['users']);
            }
        });
    }
    function init() {
        $('#id_name').on('input',getUsers);
    }
    return {
        'init' : init,
    };
})();
$(document).ready(searchUsers.init);
