// Hive Instashow System
// Copyright (C) 2008-2012 Hive Solutions Lda.
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
// __copyright__ = Copyright (c) 2010-2012 Hive Solutions Lda.
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

        // retrieves the reference to the top level window component
        // to be able to access top level elements
        var _window = jQuery(window);
        var _html = jQuery("html");

        // ensures that no overflow exists for the current html component
        // in display for the current structure
        _html.css("overflow-y", "auto");

        // retrieves the reference to the complete set of photos
        // and images to be used for manipulation
        var photos = jQuery(".photo", matchedObject);
        var images = jQuery("img", photos);

        // creates the pages panel and add it to the currently
        // matched object for reference
        var pages = jQuery("<div class=\"pages\"></div>")
        matchedObject.append(pages);

        // creates a reference to the holder of the images in the
        // current structure and adds it to the matched object
        var holder = jQuery("<div class=\"holder\"></div>")
        matchedObject.append(holder);

        // adds the complete set of photos to the holder in order
        // to store them for latter usage
        holder.append(photos);

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

        // iterates over each of the photos to start creating the
        // various pages that comprise the slideshow
        photos.each(function(index, element) {
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

        // registers for the resize event in the window to be
        // able to run the update function in them
        _window.resize(function() {
                    update();
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
            var images = jQuery(".page img", pages);

            // iterates over all the images to resize them into the
            // proper size as defined by the current viewport
            images.each(function(index, element) {
                        /// retrieves the current element (image) in iteration
                        var _element = jQuery(this);

                        // retrieves the currently defined height and width,
                        // should have been previously loaded
                        var _height = _element.attr("data-height");
                        var _width = _element.attr("data-width");
                        _height = parseInt(_height);
                        _width = parseInt(_width);

                        // calculates the rations for the height and the width
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
                    });

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

        // creates the interval that will be used for the sliding of the
        // slideshow element
        setInterval(function() {
                    // retrieves the reference to the pages and to the image
                    // elements that are going to be used in the positioning
                    var pages = jQuery(".pages", matchedObject);
                    var images = jQuery(".page img", pages);

                    // retrievs the current status of the matched object as
                    // a set of position and count values
                    var position = matchedObject.data("position");
                    var count = matchedObject.data("count");

                    // retrieves the reference to the first image and
                    // retrieves its height for reference
                    var image = jQuery(images[0]);
                    var height = image.height();

                    // calculates the next position in the slideshow and uses it
                    // to calculate the apropriate scroll top position
                    var nextPosition = position + 1 >= count ? 0 : position + 1;
                    var scrollTop = nextPosition * height;

                    // retrieves the reference to both the current and the next
                    // pages in the slideshow, to be able to use them in the
                    // cross fade effect
                    var current = jQuery(".page:nth-child(" + (position + 1)
                                    + ")", pages);
                    var next = jQuery(".page:nth-child(" + (nextPosition + 1)
                                    + ")", pages);

                    // runs the animation of the pages element "moving" the
                    // scrolling top of the element to the new scroll top
                    pages.animate({
                                scrollTop : scrollTop + "px"
                            }, {
                                duration : 1000
                            });

                    // hides the next panel and fade in and out the
                    // next and current panels (creating the cross fade
                    // effect for optimal experience)
                    next.hide();
                    next.fadeIn(1000);
                    current.fadeOut(1000, function() {
                                current.show();
                            });

                    // updates the current status of the matched object
                    // with the next position of the slideshow
                    matchedObject.data("position", nextPosition);
                }, 10000);

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
            // retrieves the reference to the top level
            // body element to apply the components in it
            var _body = jQuery("body");

            // applies the various plugins to the body element
            // this is considered the initial apply operation
            // for the section specific plugins
            _body.instashow_apply();

            // registers for the applied event on the body to be
            // notified of new apply operations and react to them
            // in the sense of applying the specifics
            _body.bind("applied", function(event, base) {
                        base.instashow_apply();
                    });
        });
