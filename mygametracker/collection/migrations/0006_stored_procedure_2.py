from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('collection', '0005_stored_procedure'),
    ]

    operations = [
        migrations.RunSQL(
            """
            CREATE DEFINER=`root`@`localhost` PROCEDURE `GeneratePlayedGamesCollection`(IN `userId` INT)
            BEGIN
                DECLARE done INT DEFAULT FALSE;
                DECLARE gameId INT;
                DECLARE existingCollectionId INT;
            
                -- Cursor to iterate over games played by the user
                DECLARE gamesCursor CURSOR FOR
                    SELECT game_id_id
                    FROM stats_usergameplatform
                    WHERE user_id_id = userId AND status = '1';
            
                -- Declare continue handler to exit loop
                DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
            
                -- Check if the collection already exists
                SELECT collection_id INTO existingCollectionId
                FROM collection_collection
                WHERE user_id_id = userId AND type = 3
                LIMIT 1;
            
                IF existingCollectionId IS NOT NULL THEN
                    -- Update the existing collection date
                    UPDATE collection_collection
                    SET date_modified = NOW()
                    WHERE collection_id = existingCollectionId;
            
                    -- Update the games inside the existing collection
                    DELETE FROM collection_collection_game_collection
                    WHERE collection_id = existingCollectionId;
            
                    OPEN gamesCursor;
            
                    read_loop: LOOP
                        FETCH gamesCursor INTO gameId;
                        IF done THEN
                            LEAVE read_loop;
                        END IF;
            
                        -- Add games to the collection
                        INSERT INTO collection_collection_game_collection (collection_id, game_id)
                        VALUES (existingCollectionId, gameId);
                    END LOOP;
            
                    CLOSE gamesCursor;
                ELSE
                    -- Create a new collection for the user
                    INSERT INTO collection_collection (user_id_id, name, description, type, date_modified)
                    VALUES (userId, 'Played Games', 'Auto-generated', 3, NOW());
            
                    -- Get the last inserted collection_id
                    SET @collectionId = LAST_INSERT_ID();
            
                    OPEN gamesCursor;
            
                    read_loop: LOOP
                        FETCH gamesCursor INTO gameId;
                        IF done THEN
                            LEAVE read_loop;
                        END IF;
            
                        -- Add games to the collection
                        INSERT INTO collection_collection_game_collection (collection_id, game_id)
                        VALUES (@collectionId, gameId);
                    END LOOP;
            
                    CLOSE gamesCursor;
                END IF;
            END;
            
            CREATE DEFINER=`root`@`localhost` PROCEDURE `GenerateCompletedGamesCollection`(IN `userId` INT)
            BEGIN
                DECLARE done INT DEFAULT FALSE;
                DECLARE gameId INT;
                DECLARE existingCollectionId INT;
            
                -- Cursor to iterate over games played by the user
                DECLARE gamesCursor CURSOR FOR
                    SELECT game_id_id
                    FROM stats_usergameplatform
                    WHERE user_id_id = userId AND status = '2';
            
                -- Declare continue handler to exit loop
                DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
            
                -- Check if the collection already exists
                SELECT collection_id INTO existingCollectionId
                FROM collection_collection
                WHERE user_id_id = userId AND type = 4
                LIMIT 1;
            
                IF existingCollectionId IS NOT NULL THEN
                    -- Update the existing collection date
                    UPDATE collection_collection
                    SET date_modified = NOW()
                    WHERE collection_id = existingCollectionId;
            
                    -- Update the games inside the existing collection
                    DELETE FROM collection_collection_game_collection
                    WHERE collection_id = existingCollectionId;
            
                    OPEN gamesCursor;
            
                    read_loop: LOOP
                        FETCH gamesCursor INTO gameId;
                        IF done THEN
                            LEAVE read_loop;
                        END IF;
            
                        -- Add games to the collection
                        INSERT INTO collection_collection_game_collection (collection_id, game_id)
                        VALUES (existingCollectionId, gameId);
                    END LOOP;
            
                    CLOSE gamesCursor;
                ELSE
                    -- Create a new collection for the user
                    INSERT INTO collection_collection (user_id_id, name, description, type, date_modified)
                    VALUES (userId, 'Completed Games', 'Auto-generated', 4, NOW());
            
                    -- Get the last inserted collection_id
                    SET @collectionId = LAST_INSERT_ID();
            
                    OPEN gamesCursor;
            
                    read_loop: LOOP
                        FETCH gamesCursor INTO gameId;
                        IF done THEN
                            LEAVE read_loop;
                        END IF;
            
                        -- Add games to the collection
                        INSERT INTO collection_collection_game_collection (collection_id, game_id)
                        VALUES (@collectionId, gameId);
                    END LOOP;
            
                    CLOSE gamesCursor;
                END IF;
            END;
            """
        ),
    ]
