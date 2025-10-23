import React from 'react';
import './ResultList.css';

const ResultList = ({ results, onDeleteResult, onClearResults }) => {
    return (
        <div className='result-list-wrapper'>
            <h3 className='result-list-header'>Results</h3>

            <div className='result-list-items'>
                {results.length === 0 && (
                    <span className='no-results'>No results yet.</span>
                )}
                {results.map(result => (
                    <div key={result.id} className='result-item'>
                        <span className='result-item-name' title={result.name}>
                            {result.name}
                        </span>

                        <div className='result-item-actions'>
                            {result.reportUrl && (
                                <button
                                    className="btn-view"
                                    title="View Report"
                                    onClick={() => window.open(result.reportUrl, '_blank')}
                                >
                                    View
                                </button>
                            )}

                            <button
                                onClick={() => onDeleteResult(result.id)}
                                title="Delete Result"
                            >
                                ❌
                            </button>
                        </div>
                    </div>
                ))}
            </div>

            <button
                className='button clear-results-button'
                onClick={onClearResults}
                disabled={results.length === 0}
            >
                Clear All Results
            </button>
        </div>
    );
};

export default ResultList;