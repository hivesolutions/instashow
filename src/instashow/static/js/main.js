// Hive Instashow System
// Copyright (C) 2008-2015 Hive Solutions Lda.
//
// This file is part of Hive Instashow System.
//
// Hive Instashow System is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// Hive Instashow System is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with Hive Instashow System. If not, see <http://www.gnu.org/licenses/>.

// __author__    = João Magalhães <joamag@hive.pt>
// __version__   = 1.0.0
// __revision__  = $LastChangedRevision$
// __date__      = $LastChangedDate$
// __copyright__ = Copyright (c) 2008-2015 Hive Solutions Lda.
// __license__   = GNU General Public License (GPL), Version 3

(function(jQuery) {
    jQuery.fn.uinstashow = function(options) {
        // sets the jquery matched object
        var matchedObject = this;

        // returns immediately in case no instashow exists
        // for the current selection structure
        if (matchedObject.length == 0) {
            return;
        }

        // tries to retrieve the currently defined timeout between
        // images for the instashow service
        var timeout = matchedObject.attr("data-timeout") || 10000;
        timeout = parseInt(timeout);

        // retrieves the reference to the top level window component
        // to be able to access top level elements
        var _window = jQuery(window);
        var _document = jQuery(document)
        var _html = jQuery("html");

        // ensures that no overflow exists for the current html component
        // in display for the current structure
        _html.css("overflow-y", "auto");

        // retrieves the reference to the initial page and adds the page
        // class into it to be able to convert it
        var initial = jQuery(".initial", matchedObject);
        initial.addClass("page");

        // retrieves the reference to the complete set of items
        // and images to be used for manipulation
        var items = jQuery(".item", matchedObject);
        var images = jQuery("img, video", items);
        images = images.filter(":not(.banner)");

        // creates the pages panel and add it to the currently
        // matched object for reference
        var pages = jQuery("<div class=\"pages\"></div>");
        matchedObject.append(pages);

        // creates a reference to the holder of the images in the
        // current structure and adds it to the matched object
        var holder = jQuery("<div class=\"holder\"></div>")
        matchedObject.append(holder);

        // adds the complete set of items to the holder in order
        // to store them for latter usage
        holder.append(items);

        // adds the the initial page at the begining of the pages
        // section (it's going to be the first one)
        pages.append(initial);

        // iterates over each of the images in the container to update
        // the values of their original sizes
        images.each(function(index, element) {
                    // retrieves the reference to the current image element
                    // to be able to set its original size
                    var _element = jQuery(this);

                    // retrieve the size of the image as both height
                    // and width to change the attribute storage for it
                    var height = _element.height() || 640;
                    var width = _element.width() || 640;

                    // updates the height and the width of the current
                    // element to the new height and width dimensions
                    _element.attr("data-height", height);
                    _element.attr("data-width", width);
                });

        // iterates over each of the items to start creating the
        // various pages that comprise the slideshow
        items.each(function(index, element) {
                    // retrieves the current element and creates a
                    // page element for it
                    var _element = jQuery(this);
                    var page = jQuery("<div class=\"page\"></div>");
                    pages.append(page);

                    // clones the current photo element and adds
                    // the contents of it to the currently created
                    // page element (repects the current photo)
                    var photoClone = _element.clone();
                    page.append(photoClone);
                });

        // creates the update function that update and positions
        // the current layout according to the current constraints
        var update = function() {
            // retrieves the currently update height and width
            // of the window component to be used in the resizing
            var height = _window.height();
            var width = _window.width();

            // retrieves the refenrece to the pages element and to
            // the complete set of images to be displayed
            var pages = jQuery(".pages", matchedObject);
            var pageList = jQuery(".page", pages);
            var images = jQuery(".page img:not(), .page video", pages);
            images = images.filter(":not(.banner)");

            // iterates over all the images to resize them into the
            // proper size as defined by the current viewport
            images.each(function(index, element) {
                        // retrieves the current element (image) in iteration
                        // and the reference to the associated page element
                        var _element = jQuery(this);
                        var page = _element.parents(".page");

                        // retrieves the currently defined height and width,
                        // should have been previously loaded
                        var _height = _element.attr("data-height");
                        var _width = _element.attr("data-width");
                        _height = parseInt(_height);
                        _width = parseInt(_width);

                        // calculates the ratios for the height and the width
                        // according to the heights and widths of both the window
                        // and the images in iteration
                        var ratioH = height / _height;
                        var ratioW = width / _width;

                        // calculates the ration to be applied as the smallest of
                        // both the height and the width rations
                        var ratio = ratioH < ratioW ? ratioH : ratioW;

                        // updates the element and the pages height and width values
                        // according to the selected ratio values
                        _element.height(_height * ratio);
                        _element.width(_width * ratio);
                        pages.height(_height * ratio);
                        pages.width(_width * ratio);
                        pageList.height(_height * ratio);
                        pageList.width(_width * ratio);
                    });

            // in case there's no images available in the current system
            // this is a special case and the size is updated using a differrent
            // strategy to avoid problems
            if (images.length == 0) {
                pages.height(height);
                pages.width(width);
                pageList.height(height);
                pageList.width(width);
            }

            // retrieves the values for position and image count for the
            // matched object as defined in its data value
            var position = matchedObject.data("position");
            var count = matchedObject.data("count");

            // retrieves the current image (first imge) and its defined heigh value
            // to be used for the scroll top calculus
            var image = jQuery(images[0]);
            var height = image.height();

            // calculates the scroll top position from the current position and the
            // "normal" height value for each element and set the new scroll top
            var scrollTop = position * height;
            pages.scrollTop(scrollTop);
        };

        var refreshPhotos = function() {
            // retrieves the currently define url for the instashow update
            // and uses it for the update operation
            var url = matchedObject.attr("data-url");
            jQuery.ajax({
                        url : url,
                        success : function(data) {
                            // in case no valid data has been received (probably due
                            // to a problem in the communication) the retrieval is
                            // ignored and the function returns immediately
                            if (!data) {
                                return;
                            }

                            // retrieves the current position and in case it's
                            // not the first one returns immediately cannot change
                            // the contents of the instashow after the first picture
                            var position = matchedObject.data("position");
                            if (position != 0) {
                                return;
                            }

                            // retrieves the complete set of pages that are displaying
                            // an image and then removes then (no longer needed)
                            var images = jQuery(".page img, .page video", pages);
                            images = images.filter(":not(.banner)");
                            var pagesList = images.parents(".page");
                            pagesList.remove();

                            // iterates over all the keys available for the data
                            // to be able to creates the page for their representation
                            for (var key in data) {
                                // retrieves the media information for the current
                                // key in iteration to be display in the screen
                                var media = data[key];

                                // in case the current value in iteration is not a valid
                                // object structure it must be ignore to avoid problems
                                if (typeof media != "object") {
                                    continue;
                                }

                                // verifies the type of the current media and then uses it
                                // to retrieve the proper reference to the resource object
                                var isVideo = media.type == "video";
                                var resource = isVideo
                                        ? media.videos.standard_resolution
                                        : media.images.standard_resolution;

                                // retrieves the proper caption string value for the media
                                // taking into account if such value is defined properly,
                                // defaulting to an empty string otherwise
                                var caption = media.caption
                                        ? media.caption.text
                                        : "";

                                // creates the element that will contain the item
                                // elements using the provided standard resolution url
                                // note that a video or image is created according to
                                // the defined type in the media object
                                var item = isVideo
                                        ? jQuery("<div class=\"item\">"
                                                + "<video src=\""
                                                + resource.url
                                                + "\" loop=\"1\"></video>"
                                                + "</div>")
                                        : jQuery("<div class=\"item\">"
                                                + "<img src=\"" + resource.url
                                                + "\" />" + "</div>");

                                // creates the labels box that is going to be used
                                // to display some information about the author
                                var box = jQuery("<div class=\"box\">"
                                        + "<div class=\"left\">"
                                        + "<h2 class=\"double\">" + caption
                                        + "</h2>" + "</div>"
                                        + "<div class=\"right\">" + "<h2>@"
                                        + media.user.username + "</h2>"
                                        + "<h3>" + media.user.full_name
                                        + "</h3>" + "</div>" + "</div>");
                                item.append(box)

                                // creates the page element and adds it to the
                                // list of pages for the current structure
                                var page = jQuery("<div class=\"page\"></div>");
                                pages.append(page);

                                // adds the newly created item element to the new
                                // page sets it as the only contents of it
                                page.append(item);

                                // retrieve the image component out of the item
                                // element to be used in attribute changes
                                var image = jQuery("img, video", item);
                                image = image.filter(":not(.banner)");

                                // retrieve the size of the image as both height
                                // and width to change the attribute storage for it
                                var height = resource.height || 640;
                                var width = resource.width || 640;

                                // updates the height and the width of the current
                                // element to the new height and width dimensions
                                image.attr("data-height", height);
                                image.attr("data-width", width);
                            }

                            // retrieves the current available list of pages for the
                            // current matched object, the ones currently in display
                            var pageList = jQuery(".pages > .page",
                                    matchedObject);

                            // updates the count of pages for the matched object, taking
                            // into account the new pages to be displayed
                            matchedObject.data("count", pageList.length)
                            update();
                        }
                    });
        };

        var setPosition = function(nextPosition, duration) {
            // tries to retrieve the pending (animation) flag and in
            // case the value is set returns immediately no override
            // in the current pipeline of animations, then sets the
            // flag so that no more animations are allowed
            var pending = matchedObject.data("pending");
            if (pending) {
                return;
            }
            matchedObject.data("pending", true);

            // sets the initial value for the duration of the animation
            // in case the value has not been provided
            duration = duration || 1000;

            // retrieves the reference to the pages and to the image
            // elements that are going to be used in the positioning
            var pages = jQuery(".pages", matchedObject);
            var images = jQuery(".page img, .page video", pages);
            images = images.filter(":not(.banner)");

            // retrievs the current status of the matched object as
            // a set of position and count values
            var position = matchedObject.data("position");
            var count = matchedObject.data("count");

            // retrieves the reference to the first image and
            // retrieves its height for reference
            var image = jQuery(images[0]);
            var height = image.height();

            // calculates the scroll top position in pixels that is going
            // to be used in the scroll animation (should be an integer)
            var scrollTop = nextPosition * height;

            // in case the next position is the initial one must refresh
            // the photos to the new ones (iteration cycle), note that
            // this operation is delayed to the end of the transition so
            // that no flickering problems occur while changing images
            nextPosition == 0 && setTimeout(function() {
                        refreshPhotos();
                    }, duration);

            // in case the current position is the same as the next one
            // returns immediately to avoid the cross fade effect to the
            // same index (this is not wanted as the screen flicks)
            if (position == nextPosition) {
                return;
            }

            // retrieves the reference to both the current and the next
            // pages in the slideshow, to be able to use them in the
            // cross fade effect
            var current = jQuery(".page:nth-child(" + (position + 1) + ")",
                    pages);
            var next = jQuery(".page:nth-child(" + (nextPosition + 1) + ")",
                    pages);

            // runs the animation of the pages element "moving" the
            // scrolling top of the element to the new scroll top
            pages.animate({
                        scrollTop : scrollTop + "px"
                    }, {
                        duration : duration
                    });

            // hides the next panel and fade in and out the
            // next and current panels (creating the cross fade
            // effect for optimal experience)
            next.hide();
            next.fadeIn(duration);
            current.fadeOut(duration, function() {
                        current.show();
                        var video = jQuery("video", current);
                        video.length && video[0].pause();
                        matchedObject.data("pending", false);
                    });

            // tries to retrieve the video reference for the
            // next page to be display and in case it
            // exists starts playing the video
            var video = jQuery("video", next);
            video.length && video[0].play();

            // updates the current status of the matched object
            // with the next position of the slideshow
            matchedObject.data("position", nextPosition);

            // schedules the next iteration of the slideshow auto
            // loopback so that the next position is going to be
            // set after the timeout value of seconds passes
            scheduleNext();
        };

        var nextPosition = function() {
            // retrievs the current status of the matched object as
            // a set of position and count values
            var position = matchedObject.data("position");
            var count = matchedObject.data("count");

            // calculates the next position in the slideshow and calls
            // the proper function to trigger the animations and position
            var nextPosition = position + 1 >= count ? 0 : position + 1;
            setPosition(nextPosition);
        };

        var previousPosition = function() {
            // retrievs the current status of the matched object as
            // a set of position and count values
            var position = matchedObject.data("position");
            var count = matchedObject.data("count");

            // calculates the previous position in the slideshow and calls
            // the proper function to trigger the animations and position
            var previousPosition = position - 1 < 0 ? count - 1 : position - 1;
            setPosition(previousPosition);
        };

        var scheduleNext = function() {
            // retrieves the currently defined timeout reference
            // and in case it's valid clears it so that it becomes
            // invalidated (not going to be performed)
            var _timeout = matchedObject.data("timeout");
            _timeout && clearTimeout(_timeout)

            // creates the timeout function, registering it under
            // the current object to be used latter for cancelation
            _timeout = setTimeout(function() {
                        nextPosition();
                    }, timeout);
            matchedObject.data("timeout", _timeout);
        };

        // registers for the resize event in the window to be
        // able to run the update function in them
        _window.resize(onResize = function() {
            update();
        });
        matchedObject.bind("destroyed", function() {
                    _window.unbind("resize", onResize);
                });

        // registers for the key down event on the document
        // element so that it's possible to manually control
        // the flow of images/videos of the slideshow
        _document.keydown(onKeyDown = function(event) {
            var keyValue = event.keyCode ? event.keyCode : event.charCode
                    ? event.charCode
                    : event.which;
            switch (keyValue) {
                case 37 :
                case 38 :
                    previousPosition();
                    break;
                case 39 :
                case 40 :
                    nextPosition();
                    break;
            }
        });
        matchedObject.bind("destroyed", function() {
                    _document.unbind("keydown", onKeyDown);
                });

        // registers for the detroyed event on the current
        // object so that the currently registered timeout
        // is cleared avoiding any further calls
        matchedObject.bind("destroyed", function() {
                    var _timeout = matchedObject.data("timeout");
                    _timeout && clearTimeout(_timeout)
                });

        // retrieves the complete set of pages in the current object
        // this value will be used as the count of the object
        var pageList = jQuery(".pages > .page", matchedObject);

        // sets the initial position in the currently matched object
        // so that the show starts at the initial position
        matchedObject.data("position", 0);
        matchedObject.data("count", pageList.length);

        // runs the initial update operation on the show
        // to position the various images in the initial
        // position
        update();

        // schedules the initial iteration of the slideshow
        // auto loopback so that the position is going to be
        // set after the timeout value of seconds passes
        scheduleNext();
    };
})(jQuery);

(function(jQuery) {
    jQuery.fn.instashow_apply = function(options) {
        // sets the jquery matched object
        var matchedObject = this;

        // retrieves the various instashow sections
        // and registers the instashow logic
        var instashow = jQuery(".instashow", matchedObject);
        instashow.uinstashow();
    };
})(jQuery);

jQuery(document).ready(function() {
            var _body = jQuery("body");
            _body.bind("applied", function(event, base) {
                        base.instashow_apply();
                    });
        });
